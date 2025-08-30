

_ARG_LOCATION = Union[str, int, tuple[int, str]]
_TemplatePart = Union[
    tuple[Literal["STATIC"], str],
    tuple[Literal["ARG"], _ARG_LOCATION], # the str is the arg name
]


Templatizable = Callable[..., Node]


def _traverse_node(node: Node,
                   template_parts: list[_TemplatePart],
                   sentinel_objects: dict[int, _ARG_LOCATION]) -> None:

    def append_static(obj: str) -> None:
        return template_parts.append(("STATIC", obj))

    def append_arg(arg: _ARG_LOCATION) -> None:
        return template_parts.append(("ARG", arg))

    node_id = id(node)

    # note that this should stay up-to-speed with the `Node` definition
    if type(node) is tuple:
        # TagTuple
        append_static(node[0])
        for n in node[1]:
            _traverse_node(n, template_parts, sentinel_objects)
        append_static(node[2])
    elif type(node) is str:
        # Check if this string is one of our sentinels
        if node_id in sentinel_objects:
            # This is an argument placeholder - add a marker
            append_arg(sentinel_objects[node_id])
        else:
            # Regular string content
            append_static(faster_escape(node))
    elif type(node) is SafeString:
        # SafeString content - check if it's a sentinel
        if node_id in sentinel_objects:
            append_arg(sentinel_objects[node_id])
        else:
            append_static(node.safe_str)
    elif type(node) is Tag:
        append_static(node.rendered)
    elif isinstance(node, (list, GeneratorType)):
        for n in node:
            _traverse_node(n, template_parts, sentinel_objects)
    elif isinstance(node, (int, float, Decimal)):
        if node_id in sentinel_objects:
            append_arg(sentinel_objects[node_id])
        else:
            # Other types - convert to string
            append_static(str(node))
    else:
        print(node)
        raise TypeError(f"Got unexpected type for node: {type(node)}")

def _cannot_templatize_message(func: Callable[..., Any],
                               extra_message: str) -> str:
    return f"Could not templatize function '{func.__name__}'. {extra_message}"

_SHOULD_NOT_PERFORM_LOGIC = "Templatizable functions should not perform logic."
_NO_ARGS_OR_KWARGS = "Templatizable functions cannot accept *args or **kwargs."

def _probe_func(func: Templatizable, variant: Literal[1, 2, 3]) -> list[_TemplatePart]:
    # TODO: try different types of arguments...?
    sig = inspect.signature(func)
    parameters = sig.parameters

    if not parameters:
        raise ValueError("Function must have at least one parameter")

    # probe function with properly typed arguments
    # Use interned sentinel objects that we can identify by id
    sentinel_objects: dict[int, _ARG_LOCATION] = {}
    probe_args: list[Node] = []
    probe_kwargs: dict[str, Node] = {}

    sentinel: Node
    for i, (param_name, param) in enumerate(parameters.items()):
        if variant == 1:
            sentinel = f"__SENTINEL_{param_name}_{id(object())}__"
        elif variant == 2:
            sentinel = uuid4().hex
        else:
            sentinel = 1039917274618672531762351823761235 + id(object())

        sentinel_id = id(sentinel)

        if param.kind == inspect.Parameter.POSITIONAL_ONLY:
            probe_args.append(sentinel)
            sentinel_objects[sentinel_id] = i
        elif param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            probe_args.append(sentinel)
            # allow either an index or key lookup
            sentinel_objects[sentinel_id] = (i, param.name)
        elif param.kind == inspect.Parameter.KEYWORD_ONLY:
            probe_kwargs[param_name] = sentinel
            sentinel_objects[sentinel_id] = param.name
        elif param.kind == inspect.Parameter.VAR_POSITIONAL:
            raise AssertionError(_cannot_templatize_message(func, _NO_ARGS_OR_KWARGS))

        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            raise AssertionError(_cannot_templatize_message(func, _NO_ARGS_OR_KWARGS))

    try:
        template_node = func(*probe_args, **probe_kwargs)
    except Exception as e:
        raise Exception(
            e,
            AssertionError(_cannot_templatize_message(func, _SHOULD_NOT_PERFORM_LOGIC))
        )

    # traverse `Node` tree structure to find usages of arguments by id
    template_parts: list[_TemplatePart] = []

    _traverse_node(template_node, template_parts, sentinel_objects)

    return template_parts


_CoalescedPart = Union[_ARG_LOCATION, SafeString]

def _coalesce_func(func: Templatizable) -> list[_CoalescedPart]:
    template_part_lists: tuple[list[_TemplatePart], list[_TemplatePart], list[_TemplatePart]] = (
        _probe_func(func, 1),
        _probe_func(func, 2),
        _probe_func(func, 3)
    )
    assert len(template_part_lists[0]) == len(template_part_lists[1]) == len(template_part_lists[2]), _cannot_templatize_message(func, _SHOULD_NOT_PERFORM_LOGIC)

    for part_1, part_2, part_3 in zip(*template_part_lists):
        assert part_1[0] == part_2[0] == part_3[0], _cannot_templatize_message(func, _SHOULD_NOT_PERFORM_LOGIC)
        if part_1[0] == "STATIC":
            assert (part_1[1] == part_2[1] == part_3[1]), _cannot_templatize_message(func, _SHOULD_NOT_PERFORM_LOGIC)

    # convert non-argument nodes to strings and coalesce for speed
    coalesced_parts: list[_CoalescedPart] = [] # string's are for parameter names
    current_static: list[str] = []

    for part_type, content in template_part_lists[0]:
        if part_type == 'STATIC':
            current_static.append(str(content))
        else:  # ARG
            # Flush accumulated static content
            if current_static:
                coalesced_parts.append(SafeString(''.join(current_static)))
                current_static = []
            coalesced_parts.append(content)

    # Flush any remaining static content
    if current_static:
        coalesced_parts.append(SafeString(''.join(current_static)))

    return coalesced_parts

def _get_arg_val(args: tuple[Node, ...],
                 kwargs: dict[str, Node],
                 location: _ARG_LOCATION) -> Node:
    if isinstance(location, tuple):
        int_loc, str_loc = location
        if len(args) >= int_loc + 1:
            return args[int_loc]
        else:
            return kwargs[str_loc]
    elif isinstance(location, int):
        return args[location]
    else:
        return kwargs[location]


def templatize(func: Templatizable) -> Callable[..., Node]:
    coalesced_parts = _coalesce_func(func)

    def template_function(*args: Node, **kwargs: Node) -> Node:
        return [
            part if isinstance(part, SafeString) else _get_arg_val(args, kwargs, part)
            for part in coalesced_parts
        ]

    return template_function



def is_valid_node(node: Any) -> bool:
    """Check if the given object is a valid Node."""
    origin = get_origin(node)
    args = get_args(node)

    if isinstance(node, (str, SafeString, float, int, Decimal)):
        return True
    elif isinstance(node, list):
        return all(is_valid_node(item) for item in node)
    elif isinstance(node, GeneratorType):
        return all(is_valid_node(item) for item in node)
    elif isinstance(node, Tag):
        return True
    elif origin is tuple and len(args) == 3:
        # Assuming the tuple structure is (str, list[Node], str)
        tag_tuple_type = args
        if not isinstance(tag_tuple_type[0], str) or not isinstance(tag_tuple_type[2], str):
            return False
        return all(is_valid_node(item) for item in tag_tuple_type[1])
    else:
        return False


def validate_node_annotations(func: Callable) -> Callable:
    """
    Decorator to validate that all arguments annotated with Node are instances of Node.

    :param func: The function to decorate.
    :return: A wrapped function that performs validation.
    """
    from inspect import signature

    sig = signature(func)
    annotations = sig.annotations

    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        for name, value in bound_args.arguments.items():
            if name in annotations and get_origin(annotations[name]) is Union:
                args = get_args(annotations[name])
                if Node in args:
                    if not is_valid_node(value):
                        raise TypeError(f"Argument '{name}' must be a valid Node, got {type(value).__name__}")

        return func(*args, **kwargs)

    return wrapper


# Example usage
@validate_node_annotations
def process_node(node: Node) -> None:
    print(f"Processing node: {node}")


# Example nodes
root = Tag(rendered="root")
process_node(root)
