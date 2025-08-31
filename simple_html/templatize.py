import inspect
import types
import warnings
from decimal import Decimal
from types import GeneratorType
from typing import Union, Literal, Callable, Any, get_args, get_origin, Generator, ForwardRef
from uuid import uuid4

from simple_html import Node, SafeString, h1
from simple_html.core import faster_escape, Tag

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
        if node_id in sentinel_objects:
            append_arg(sentinel_objects[node_id])
        else:
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
    warn_if_invalid_annotations(func)

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
            sentinel = [id(object())]

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


def _is_valid_node_annotation(annotation: Any) -> bool:
    """Check if an annotation represents a valid Node type (recursive)."""
    # Handle ForwardRef objects
    if isinstance(annotation, ForwardRef):
        # Get the string argument from ForwardRef
        ref_name = annotation.__forward_arg__
        # Check if it refers to a valid Node type
        return ref_name in ('Node', 'Tag', 'TagTuple')

    # Handle string literals (like 'Node' in list['Node'])
    elif isinstance(annotation, str):
        return annotation in ('Node', 'Tag', 'TagTuple')

    # Direct Node type
    elif annotation == Node:
        return True

    # Basic valid Node component types
    elif annotation in (str, int, float, Decimal, SafeString, Tag):
        return True

    # Check for Union types (like Optional[Node] or Union[Node, str])
    elif (origin := get_origin(annotation)) is Union or (hasattr(types, 'UnionType') and isinstance(annotation, types.UnionType)):
        union_args = get_args(annotation)
        # All union members must be valid Node types (except None for Optional)
        return all(_is_valid_node_annotation(arg) for arg in union_args if arg is not type(None))

    # Check for tuple types - specifically TagTuple: tuple[str, tuple[Node, ...], str]
    elif get_origin(annotation) is tuple:
        type_args = get_args(annotation)
        if len(type_args) == 3:
            # TagTuple structure: (str, tuple[Node, ...], str)
            first_arg, second_arg, third_arg = type_args
            if (first_arg == str and third_arg == str and
                    get_origin(second_arg) is tuple and len(get_args(second_arg)) >= 1):
                # Check if the tuple contains Node types (like tuple[Node, ...])
                inner_args = get_args(second_arg)
                return all(_is_valid_node_annotation(arg) for arg in inner_args if arg is not ...)
        # If it's not a valid TagTuple structure, it's invalid
        return False

    # Check for generic types like list[Node], Generator[Node, None, None], etc.
    elif (origin := get_origin(annotation)) is not None:
        type_args = get_args(annotation)
        if type_args:
            # For list[Node], Generator[Node, None, None], etc.
            if origin is list:
                # All list element types must be valid Node types
                return all(_is_valid_node_annotation(arg) for arg in type_args)
            elif origin is Generator or (hasattr(origin, '__name__') and 'Generator' in str(origin)):
                # For Generator[Node, None, None], only check the first type argument
                return _is_valid_node_annotation(type_args[0]) if type_args else False
    return False


def warn_if_invalid_annotations(func: Templatizable) -> None:
    """
    Decorator to validate that the function signature only uses valid Node annotations.
    Validates at decoration time, not runtime.

    :param func: The function to decorate.
    :return: The original function if validation passes.
    :raises: TypeError if the function has invalid annotations.
    """
    sig = inspect.signature(func)

    # Check if function has at least one parameter
    if not sig.parameters:
        raise TypeError(f"Function '{func.__name__}' must have at least one parameter")

    # Check each parameter's annotation
    for param_name, param in sig.parameters.items():
        annotation = param.annotation

        # Skip parameters without annotations
        if annotation == inspect.Parameter.empty:
            continue

        # Check if annotation is valid for Node types
        if not _is_valid_node_annotation(annotation):
            warnings.warn(
                f"Parameter '{param_name}' in function '{func.__name__}' has invalid annotation: {annotation}. "
                f"Only Node-compatible types are allowed in Templatize."
            )
