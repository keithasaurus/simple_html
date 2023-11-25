from html import escape
from types import GeneratorType
from typing import Tuple, Union, Dict, List, FrozenSet, Generator, Iterable


class SafeString:
    __slots__ = ("safe_str",)

    def __init__(self, safe_str: str) -> None:
        self.safe_str = safe_str

    def __hash__(self) -> int:
        return hash(f"SafeString__{self.safe_str}")


Node = Union[
    str,
    SafeString,
    "Tag",
    "TagTuple",
    List["Node"],
    Generator["Node", None, None],
]

TagTuple = Tuple[str, Tuple[Node, ...], str]

_common_safe_keys: FrozenSet[str] = frozenset(
    {
        "alt",
        "autoplay",
        "autoplay",
        "charset",
        "checked",
        "class",
        "content",
        "contenteditable",
        "dir",
        "draggable",
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
        "sizes",
        "spellcheck",
        "src",
        "style",
        "target",
        "title",
        "type",
        "value",
        "width",
    }
)


def escape_key(k: str) -> str:
    return (
        escape(k).replace("=", "&#x3D;").replace("\\", "&#x5C;").replace("`", "&#x60;")
    )


class Tag:
    __slots__ = ("tag_start", "rendered", "closing_tag", "no_children_close")

    def __init__(self, name: str, self_closing: bool = False) -> None:
        self.tag_start = f"<{name}"
        if self_closing:
            self.closing_tag = ""
            self.no_children_close = "/>"
        else:
            self.closing_tag = f"</{name}>"
            self.no_children_close = f">{self.closing_tag}"
        self.rendered = f"{self.tag_start}{self.no_children_close}"

    def __call__(
        self, attributes: Dict[str, Union[str, SafeString, None]], *children: Node
    ) -> TagTuple:
        if attributes:
            # in this case this is faster than attrs = "".join([...])
            attrs = ""
            for key, val in attributes.items():
                if key not in _common_safe_keys:
                    key = (
                        key.safe_str if isinstance(key, SafeString) else escape_key(key)
                    )
                if isinstance(val, str):
                    attrs += f' {key}="{escape(val)}"'
                elif val is None:
                    attrs += f" {key}"
                elif isinstance(val, SafeString):
                    attrs += f' {key}="{val.safe_str}"'

            if children:
                return f"{self.tag_start}{attrs}>", children, self.closing_tag
            else:
                return f"{self.tag_start}{attrs}{self.no_children_close}", children, ""
        return f"{self.tag_start}>", children, self.closing_tag


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


def _render(nodes: Iterable[Node], strs: List[str]) -> None:
    """
    mutate a list instead of constantly rendering strings
    """
    for node in nodes:
        if type(node) is tuple:
            strs.append(node[0])
            _render(node[1], strs)
            strs.append(node[2])
        elif isinstance(node, str):
            strs.append(escape(node))
        elif isinstance(node, SafeString):
            strs.append(node.safe_str)
        elif isinstance(node, Tag):
            strs.append(node.rendered)
        elif isinstance(node, list):
            _render(node, strs)
        elif isinstance(node, GeneratorType):
            _render(node, strs)
        else:
            raise TypeError(f"Got unknown type: {type(node)}")


def render(*nodes: Node) -> str:
    results: List[str] = []
    _render(nodes, results)

    return "".join(results)
