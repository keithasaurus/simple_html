from html import escape
from types import GeneratorType
from typing import Tuple, Union, Dict, List, FrozenSet, Generator, Iterable, Any, Callable


class SafeString:
    def __init__(self, safe_str: str) -> None:
        self.safe_str = safe_str

    def __hash__(self) -> int:
        return hash(f"SafeString__{self.safe_str}")

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, SafeString) and other.safe_str == self.safe_str

    def __repr__(self) -> str:
        return f"SafeString(safe_str='{self.safe_str}')"


def faster_escape(s: str) -> str:
    """
    This is nearly duplicate of html.escape in the standard lib.
    it's a little faster because:
     - we don't check if some of the replacements are desired
     - we don't re-assign a variable many times.
    """
    return s.replace(
        "&", "&amp;"   # Must be done first!
    ).replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace('\'', "&#x27;")

Node = Union[
    str,
    SafeString,
    "Tag",
    "TagTuple",
    List["Node"],
    Generator["Node", None, None],
]

TagTuple = Tuple[str, Tuple[Node, ...], str]

_common_safe_attribute_names: FrozenSet[str] = frozenset(
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
    )

    def __init__(self, name: str, self_closing: bool = False) -> None:
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
        attributes: Dict[Union[SafeString, str], Union[str, SafeString, None]],
        *children: Node,
    ) -> Union[TagTuple, SafeString]:
        if attributes:
            # in this case this is faster than attrs = "".join([...])
            attrs = ""
            for key, val in attributes.items():
                # optimization: a large portion of attribute keys should be
                # covered by this check. It allows us to skip escaping
                # where it is not needed. Note this is for attribute names only;
                # attributes values are always escaped (when they are `str`s)
                if key not in _common_safe_attribute_names:
                    key = (
                        escape_attribute_key(key)
                        if isinstance(key, str)
                        else key.safe_str
                    )

                if isinstance(val, str):
                    attrs += f' {key}="{faster_escape(val)}"'
                elif isinstance(val, SafeString):
                    attrs += f' {key}="{val.safe_str}"'
                elif val is None:
                    attrs += f" {key}"

            if children:
                return f"{self.tag_start}{attrs}>", children, self.closing_tag
            else:
                return SafeString(f"{self.tag_start}{attrs}{self.no_children_close}")
        elif children:
            return self.tag_start_no_attrs, children, self.closing_tag
        else:
            return SafeString(self.rendered)


DOCTYPE_HTML5 = SafeString("<!doctype html>")

a = Tag("a")
abbr = Tag("abbr")
address = Tag("address")
area = Tag("area", True)
article = Tag("article")
aside = Tag("aside")
audio = Tag("audio")
b = Tag("b")
base = Tag("base", True)
bdi = Tag("bdi")
bdo = Tag("bdo")
blockquote = Tag("blockquote")
body = Tag("body")
br = Tag("br", True)
button = Tag("button")
canvas = Tag("canvas")
center = Tag("center")
caption = Tag("caption")
cite = Tag("cite")
code = Tag("code")
col = Tag("col")
colgroup = Tag("colgroup")
datalist = Tag("datalist")
dd = Tag("dd")
details = Tag("details")
del_ = Tag("del")
dfn = Tag("dfn")
div = Tag("div")
dl = Tag("dl")
dt = Tag("dt")
em = Tag("em")
embed = Tag("embed", True)
fieldset = Tag("fieldset")
figure = Tag("figure")
figcaption = Tag("figcaption")
footer = Tag("footer")
font = Tag("font")
form = Tag("form")
head = Tag("head")
header = Tag("header")
h1 = Tag("h1")
h2 = Tag("h2")
h3 = Tag("h3")
h4 = Tag("h4")
h5 = Tag("h5")
h6 = Tag("h6")
hr = Tag("hr", True)
html = Tag("html")
i = Tag("i")
iframe = Tag("iframe", True)
img = Tag("img", True)
input_ = Tag("input", True)
ins = Tag("ins")
kbd = Tag("kbd")
label = Tag("label")
legend = Tag("legend")
li = Tag("li")
link = Tag("link", True)
main = Tag("main")
mark = Tag("mark")
marquee = Tag("marquee")
math = Tag("math")
menu = Tag("menu")
menuitem = Tag("menuitem")
meta = Tag("meta", True)
meter = Tag("meter")
nav = Tag("nav")
object_ = Tag("object")
noscript = Tag("noscript")
ol = Tag("ol")
optgroup = Tag("optgroup")
option = Tag("option")
p = Tag("p")
param = Tag("param", True)
picture = Tag("picture")
pre = Tag("pre")
progress = Tag("progress")
q = Tag("q")
rp = Tag("rp")
rt = Tag("rt")
ruby = Tag("ruby")
s = Tag("s")
samp = Tag("samp")
script = Tag("script")
section = Tag("section")
select = Tag("select")
small = Tag("small")
source = Tag("source", True)
span = Tag("span")
strike = Tag("strike")
strong = Tag("strong")
style = Tag("style")
sub = Tag("sub")
summary = Tag("summary")
sup = Tag("sup")
svg = Tag("svg")
table = Tag("table")
tbody = Tag("tbody")
template = Tag("template")
textarea = Tag("textarea")
td = Tag("td")
th = Tag("th")
thead = Tag("thead")
time = Tag("time")
title = Tag("title")
tr = Tag("tr")
track = Tag("track", True)
u = Tag("u")
ul = Tag("ul")
var = Tag("var")
video = Tag("video")
wbr = Tag("wbr")


def _render(nodes: Iterable[Node], append_to_list: Callable[[str], None]) -> None:
    """
    mutate a list instead of constantly rendering strings
    """
    for node in nodes:
        if type(node) is tuple:
            append_to_list(node[0])
            _render(node[1], append_to_list)
            append_to_list(node[2])
        elif isinstance(node, SafeString):
            append_to_list(node.safe_str)
        elif isinstance(node, str):
            append_to_list(faster_escape(node))
        elif isinstance(node, Tag):
            append_to_list(node.rendered)
        elif isinstance(node, list):
            _render(node, append_to_list)
        elif isinstance(node, GeneratorType):
            _render(node, append_to_list)
        else:
            raise TypeError(f"Got unknown type: {type(node)}")


_common_safe_css_props = frozenset(
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
    styles: Dict[Union[str, SafeString], Union[str, int, float, SafeString]]
) -> SafeString:
    ret = ""
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

        ret += f"{k}:{v};"

    return SafeString(ret)


def render(*nodes: Node) -> str:
    results: List[str] = []
    _render(nodes, results.append)

    return "".join(results)
