import inspect
from decimal import Decimal
from types import GeneratorType
from typing import Any, Union, Generator, Iterable, Callable, Final, TYPE_CHECKING, Protocol, Literal, Never, cast
from uuid import uuid4


class SafeString:
    __slots__ = ("safe_str",)

    def __init__(self, safe_str: str) -> None:
        self.safe_str = safe_str

    def __hash__(self) -> int:
        return hash(("SafeString", self.safe_str))

    def __eq__(self, other: Any) -> bool:
        return type(other) is SafeString and other.safe_str == self.safe_str

    def __repr__(self) -> str:
        return f"SafeString(safe_str='{self.safe_str}')"


def faster_escape(s: str) -> str:
    """
    This is nearly duplicate of html.escape in the standard lib.
    it's a little faster because:
     - we don't check if some of the replacements are desired
     - we don't re-assign a variable many times.
    """
    if "'" not in s and '"' not in s and '<' not in s and ">" not in s and '&' not in s:
        return s

    return s.replace(
        "&", "&amp;"   # Must be done first!
    ).replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace('\'', "&#x27;")

Node = Union[
    str,
    SafeString,
    float,
    int,
    Decimal,
    list["Node"],
    Generator["Node", None, None],
    "Tag",
    "TagTuple",
]

TagTuple = tuple[str, tuple[Node, ...], str]

_common_safe_attribute_names: Final[frozenset[str]] = frozenset(
    (
        "alt",
        "autoplay",
        "charset",
        "checked",
        "class",
        "colspan",
        "content",
        "contenteditable",
        "dir",
        "draggable",
        "enctype",
        "for",
        "height",
        "hidden",
        "href",
        "hreflang",
        "http-equiv",
        "id",
        "itemprop",
        "itemscope",
        "itemtype",
        "lang",
        "loadable",
        "method",
        "name",
        "onblur",
        "onclick",
        "onfocus",
        "onkeydown",
        "onkeyup",
        "onload",
        "onselect",
        "onsubmit",
        "placeholder",
        "poster",
        "property",
        "rel",
        "rowspan",
        "sizes",
        "spellcheck",
        "src",
        "style",
        "target",
        "title",
        "type",
        "value",
        "width",
    )
)


def escape_attribute_key(k: str) -> str:
    return (
        faster_escape(k)
        .replace("=", "&#x3D;")
        .replace("\\", "&#x5C;")
        .replace("`", "&#x60;")
        .replace(" ", "&nbsp;")
    )


class Tag:
    __slots__ = (
        "tag_start",
        "closing_tag",
        "tag_start_no_attrs",
        "rendered",
        "no_children_close",
        "_repr"
    )

    def __init__(self, name: str, self_closing: bool = False) -> None:
        self._repr = f"Tag(name='{name}', self_closing={self_closing})"
        self.tag_start = f"<{name}"
        self.tag_start_no_attrs = f"{self.tag_start}>"
        self.closing_tag = f"</{name}>"
        if self_closing:
            self.no_children_close = "/>"
        else:
            self.no_children_close = f">{self.closing_tag}"
        self.rendered = f"{self.tag_start}{self.no_children_close}"

    def __call__(
        self,
        attrs_or_first_child: Union[dict[Union[SafeString, str], Union[str, SafeString, int, float, Decimal, None]], Node],
        *children: Node,
    ) -> Union[TagTuple, SafeString]:
        if isinstance(attrs_or_first_child, dict):
            # in this case this tends to be faster than attrs = "".join([...])
            attrs: list[str] = []
            for key in attrs_or_first_child:
                # seems to be faster than using .items()
                val: Union[str, SafeString, int, float, Decimal, None] = attrs_or_first_child[key]

                # optimization: a large portion of attribute keys should be
                # covered by this check. It allows us to skip escaping
                # where it is not needed. Note this is for attribute names only;
                # attributes values are always escaped (when they are `str`s)
                # key_: str
                if key not in _common_safe_attribute_names:
                    key = (
                        escape_attribute_key(key)
                        if isinstance(key, str)
                        else key.safe_str
                    )
                elif TYPE_CHECKING:
                    assert isinstance(key, str)

                if type(val) is str:
                    attrs.append(f' {key}="{faster_escape(val)}"')
                elif type(val) is SafeString:
                    attrs.append(f' {key}="{val.safe_str}"')
                elif val is None:
                    attrs.append(" " + key)
                elif isinstance(val, (int, float, Decimal)):
                    attrs.append(f' {key}="{val}"')

            if children:
                return self.tag_start + "".join(attrs) + ">", children, self.closing_tag
            else:
                return SafeString(self.tag_start + "".join(attrs) + self.no_children_close)
        else:
            return self.tag_start_no_attrs, (attrs_or_first_child,) + children, self.closing_tag

    def __repr__(self) -> str:
        return self._repr


def _render(nodes: Iterable[Node], append_to_list: Callable[[str], None]) -> None:
    """
    mutate a list instead of constantly rendering strings
    """
    for node in nodes:
        if type(node) is tuple:
            append_to_list(node[0])
            _render(node[1], append_to_list)
            append_to_list(node[2])
        elif type(node) is SafeString:
            append_to_list(node.safe_str)
        elif type(node) is str:
            append_to_list(faster_escape(node))
        elif type(node) is Tag:
            append_to_list(node.rendered)
        elif type(node) is list or type(node) is GeneratorType:
            _render(node, append_to_list)
        elif isinstance(node, (int, float, Decimal)):
            append_to_list(str(node))
        else:
            raise TypeError(f"Got unknown type: {type(node)}")


_common_safe_css_props: Final[frozenset[str]] = frozenset(
    (
        "color",
        "border",
        "margin",
        "font-style",
        "transform",
        "background-color",
        "align-content",
        "align-items",
        "align-self",
        "all",
        "animation",
        "animation-delay",
        "animation-direction",
        "animation-duration",
        "animation-fill-mode",
        "animation-iteration-count",
        "animation-name",
        "animation-play-state",
        "animation-timing-function",
        "backface-visibility",
        "background",
        "background-attachment",
        "background-blend-mode",
        "background-clip",
        "background-color",
        "background-image",
        "background-origin",
        "background-position",
        "background-repeat",
        "background-size",
        "border",
        "border-bottom",
        "border-bottom-color",
        "border-bottom-left-radius",
        "border-bottom-right-radius",
        "border-bottom-style",
        "border-bottom-width",
        "border-collapse",
        "border-color",
        "border-image",
        "border-image-outset",
        "border-image-repeat",
        "border-image-slice",
        "border-image-source",
        "border-image-width",
        "border-left",
        "border-left-color",
        "border-left-style",
        "border-left-width",
        "border-radius",
        "border-right",
        "border-right-color",
        "border-right-style",
        "border-right-width",
        "border-spacing",
        "border-style",
        "border-top",
        "border-top-color",
        "border-top-left-radius",
        "border-top-right-radius",
        "border-top-style",
        "border-top-width",
        "border-width",
        "bottom",
        "box-shadow",
        "box-sizing",
        "caption-side",
        "caret-color",
        "@charset",
        "clear",
        "clip",
        "clip-path",
        "color",
        "column-count",
        "column-fill",
        "column-gap",
        "column-rule",
        "column-rule-color",
        "column-rule-style",
        "column-rule-width",
        "column-span",
        "column-width",
        "columns",
        "content",
        "counter-increment",
        "counter-reset",
        "cursor",
        "direction",
        "display",
        "empty-cells",
        "filter",
        "flex",
        "flex-basis",
        "flex-direction",
        "flex-flow",
        "flex-grow",
        "flex-shrink",
        "flex-wrap",
        "float",
        "font",
        "@font-face",
        "font-family",
        "font-kerning",
        "font-size",
        "font-size-adjust",
        "font-stretch",
        "font-style",
        "font-variant",
        "font-weight",
        "grid",
        "grid-area",
        "grid-auto-columns",
        "grid-auto-flow",
        "grid-auto-rows",
        "grid-column",
        "grid-column-end",
        "grid-column-gap",
        "grid-column-start",
        "grid-gap",
        "grid-row",
        "grid-row-end",
        "grid-row-gap",
        "grid-row-start",
        "grid-template",
        "grid-template-areas",
        "grid-template-columns",
        "grid-template-rows",
        "height",
        "hyphens",
        "@import",
        "justify-content",
        "@keyframes",
        "left",
        "letter-spacing",
        "line-height",
        "list-style",
        "list-style-image",
        "list-style-position",
        "list-style-type",
        "margin",
        "margin-bottom",
        "margin-left",
        "margin-right",
        "margin-top",
        "max-height",
        "max-width",
        "@media",
        "min-height",
        "min-width",
        "object-fit",
        "object-position",
        "opacity",
        "order",
        "outline",
        "outline-color",
        "outline-offset",
        "outline-style",
        "outline-width",
        "overflow",
        "overflow-x",
        "overflow-y",
        "padding",
        "padding-bottom",
        "padding-left",
        "padding-right",
        "padding-top",
        "page-break-after",
        "page-break-before",
        "page-break-inside",
        "perspective",
        "perspective-origin",
        "pointer-events",
        "position",
        "quotes",
        "right",
        "scroll-behavior",
        "table-layout",
        "text-align",
        "text-align-last",
        "text-decoration",
        "text-decoration-color",
        "text-decoration-line",
        "text-decoration-style",
        "text-indent",
        "text-justify",
        "text-overflow",
        "text-shadow",
        "text-transform",
        "top",
        "transform",
        "transform-origin",
        "transform-style",
        "transition",
        "transition-delay",
        "transition-duration",
        "transition-property",
        "transition-timing-function",
        "user-select",
        "vertical-align",
        "visibility",
        "white-space",
        "width",
        "word-break",
        "word-spacing",
        "word-wrap",
        "writing-mode",
        "z-index",
    )
)



def render_styles(
    styles: dict[Union[str, SafeString], Union[str, int, float, Decimal, SafeString]]
) -> SafeString:
    ret: list[str] = []
    app = ret.append
    for k, v in styles.items():
        if k not in _common_safe_css_props:
            if isinstance(k, SafeString):
                k = k.safe_str
            else:
                k = faster_escape(k)

        if isinstance(v, SafeString):
            v = v.safe_str
        elif isinstance(v, str):
            v = faster_escape(v)
        # note that ints and floats pass through these condition checks

        app(f"{k}:{v};")

    return SafeString("".join(ret))


def render(*nodes: Node) -> str:
    results: list[str] = []
    _render(nodes, results.append)

    return "".join(results)


_ARG_LOCATION = Union[str, int, tuple[int, str]]
_TemplatePart = Union[
    tuple[Literal["STATIC"], str],
    tuple[Literal["ARG"], _ARG_LOCATION], # the str is the arg name
]


class Templatizable(Protocol):
    def __call__(self, *args: Node, **kwargs: Node) -> Node:
        ...

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
            # Create a unique string sentinel and intern it so we can find it by identity
            sentinel = f"__SENTINEL_{param_name}_{id(object())}__"
        elif variant == 2:
            # Create a unique string sentinel and intern it so we can find it by identity
            sentinel = uuid4().hex
        else:
            # Create a unique string sentinel and intern it so we can find it by identity
            sentinel = 1039917274618672531762351823761235 + id(object())

        sentinel_id = id(sentinel)

        # Determine how to pass this parameter
        if param.kind == inspect.Parameter.POSITIONAL_ONLY:
            probe_args.append(sentinel)
            sentinel_objects[sentinel_id] = i
        elif param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            # For mixed parameters, we could pass as positional or keyword
            # Let's pass as positional if it's among the first parameters
            probe_args.append(sentinel)
            sentinel_objects[sentinel_id] = (i, param.name)
        elif param.kind == inspect.Parameter.KEYWORD_ONLY:
            probe_kwargs[param_name] = sentinel
            sentinel_objects[sentinel_id] = param.name
        elif param.kind == inspect.Parameter.VAR_POSITIONAL:
            raise AssertionError(_cannot_templatize_message(func, _NO_ARGS_OR_KWARGS))

        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            raise AssertionError(_cannot_templatize_message(func, _NO_ARGS_OR_KWARGS))

    try:
        # Call function with both args and kwargs
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
        return cast(Node, [
            part if isinstance(part, SafeString) else _get_arg_val(args, kwargs, part)
            for part in coalesced_parts
        ])

    return template_function


def prerender(*nodes: Node) -> SafeString:
    return SafeString(render(*nodes))
