from decimal import Decimal
from functools import lru_cache
from types import GeneratorType
from typing import Any, Union, Generator, Iterable, Callable, Final, TYPE_CHECKING


def _get_caching_escape_func(
        func: Callable[[str], str],
        maxsize: int | None,
        max_string_length: int | None
) -> Callable[[str], str]:
    """
    @param maxsize: maximum number of entries in the lru_cache (use `None` for no maximum -- not recommended)
    @param max_string_length: maximum length of the strings for which we'll use the cache. Caching lots of very long strings
        could result in heavy memory consumption
    """
    _cache_escape = lru_cache(maxsize=maxsize)(func)

    if max_string_length is not None:
        def inner(s: str) -> str:
            if len(s) > max_string_length:
                return func(s)
            else:
                return _cache_escape(s)
        return inner
    else:
         return _cache_escape


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


_val_cache_escape = _get_caching_escape_func(faster_escape,
                                             max_string_length=200,
                                             maxsize=20000)


_str_cache_escape = _get_caching_escape_func(faster_escape,
                                             max_string_length=2000,
                                             maxsize=10000)

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

_key_cache_escape = _get_caching_escape_func(escape_attribute_key,
                                             maxsize=2000,
                                             # length of 100 should be extremely rare
                                             max_string_length=100)


AttrKey = Union[SafeString, str]
AttrValue = Union[str, SafeString, int, float, Decimal, None]

@lru_cache(maxsize=10000)
def process_attribute(key: AttrKey, val: AttrValue) -> str:
    if key not in _common_safe_attribute_names:
        key = (
            _key_cache_escape(key)
            if isinstance(key, str)
            else key.safe_str
        )
    elif TYPE_CHECKING:
        assert isinstance(key, str)

    if type(val) is str:
        return f' {key}="{_val_cache_escape(val)}"'
    elif type(val) is SafeString:
        return f' {key}="{val.safe_str}"'
    elif val is None:
        return " " + key
    elif isinstance(val, (int, float, Decimal)):
        return f' {key}="{val}"'
    return ""

class Tag:
    __slots__ = (
        "tag_start",
        "closing_tag",
        "tag_start_no_attrs",
        "rendered",
        "no_children_close",
        "_repr",
    )

    def __init__(self, name: str, self_closing: bool = False) -> None:
        self._repr: str = f"Tag(name='{name}', self_closing={self_closing})"
        self.tag_start: str = f"<{name}"
        self.tag_start_no_attrs: str = f"{self.tag_start}>"
        self.closing_tag: str = f"</{name}>"
        if self_closing:
            self.no_children_close: str = "/>"
        else:
            self.no_children_close = f">{self.closing_tag}"
        self.rendered: str = f"{self.tag_start}{self.no_children_close}"

    def __call__(
        self,
        attrs_or_first_child: Union[dict[AttrKey, AttrValue], Node],
        *children: Node,
    ) -> Union[TagTuple, SafeString]:
        if isinstance(attrs_or_first_child, dict):
            tag_and_attrs: str = self.tag_start + "".join([
                # runs faster than .items() in my experience
                process_attribute(k, attrs_or_first_child[k])
                for k in attrs_or_first_child
            ])

            if children:
                return tag_and_attrs + ">", children, self.closing_tag
            else:
                return SafeString(tag_and_attrs + self.no_children_close)
        else:
            return self.tag_start_no_attrs, (attrs_or_first_child,) + children, self.closing_tag

    def __repr__(self) -> str:
        return self._repr


def _render(nodes: Iterable[Node],
            append_to_list: Callable[[str], None],
            escape_func: Callable[[str], str]) -> None:
    """
    mutate a list instead of constantly rendering strings
    """
    for node in nodes:
        if type(node) is tuple:
            append_to_list(node[0])
            _render(node[1], append_to_list, escape_func)
            append_to_list(node[2])
        elif type(node) is SafeString:
            append_to_list(node.safe_str)
        elif type(node) is str:
            append_to_list(escape_func(node))
        elif type(node) is Tag:
            append_to_list(node.rendered)
        elif type(node) is list or type(node) is GeneratorType:
            _render(node, append_to_list, escape_func)
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


def render(*nodes: Node, escape_func: Callable[[str], str] = _str_cache_escape) -> str:
    results: list[str] = []
    _render(nodes, results.append, escape_func)

    return "".join(results)


def prerender(*nodes: Node, escape_func: Callable[[str], str] = _str_cache_escape) -> SafeString:
    return SafeString(render(*nodes, escape_func=escape_func))
