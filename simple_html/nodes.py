from dataclasses import dataclass
from typing import Tuple, Union, Optional

Attribute = Tuple[str, str]

SafeStringAlias = Tuple[str]


def SafeString(x: str) -> SafeStringAlias:
    return (x,)


Node = Union[str, SafeStringAlias, "Tag", "TagBase", "AttrsTag", "TagNoAttrs", "FlatGroup", None]


class FlatGroup:
    """
    The intention is to be able to group a number of nodes without enveloping them
    in a container. Same idea as React's fragments.
    """

    def __init__(self, *nodes: Node) -> None:
        self.nodes = nodes


Tag = Tuple["TagBase", dict[str, str], Tuple[Node, ...]]
TagNoAttrs = Tuple["TagBase", Tuple[Node, ...]]


class AttrsTag:
    __slots__ = ("tag_base", "attributes")

    def __init__(self,
                 tag_base: "TagBase",
                 attributes: dict[str, str]) -> None:
        self.tag_base = tag_base
        self.attributes = attributes

    def __call__(self, *children: Node) -> Tag:
        return self.tag_base, self.attributes, children


@dataclass(frozen=True)
class TagBase:
    # we want these to be frozen because the same TagBase is used for all elements with
    # the same tag
    name: str
    self_closes: bool = False

    def __call__(self, *children: Node) -> TagNoAttrs:
        return self, children

    def attrs(self, attributes: dict[str, str]) -> AttrsTag:
        return AttrsTag(self, attributes)


a = TagBase("a")
abbr = TagBase("abbr")
address = TagBase("address")
area = TagBase("area", True)
article = TagBase("article")
aside = TagBase("aside")
audio = TagBase("audio")
b = TagBase("b")
base = TagBase("base", True)
bdi = TagBase("bdi")
bdo = TagBase("bdo")
blockquote = TagBase("blockquote")
body = TagBase("body")
br = TagBase("br", True)
button = TagBase("button")
canvas = TagBase("canvas")
center = TagBase("center")
caption = TagBase("caption")
cite = TagBase("cite")
code = TagBase("code")
col = TagBase("col")
colgroup = TagBase("colgroup")
datalist = TagBase("datalist")
dd = TagBase("dd")
details = TagBase("details")
del_ = TagBase("del")
dfn = TagBase("dfn")
div = TagBase("div")
dl = TagBase("dl")
dt = TagBase("dt")
em = TagBase("em")
embed = TagBase("embed", True)
fieldset = TagBase("fieldset")
figure = TagBase("figure")
figcaption = TagBase("figcaption")
footer = TagBase("footer")
font = TagBase("font")
form = TagBase("form")
head = TagBase("head")
header = TagBase("header")
h1 = TagBase("h1")
h2 = TagBase("h2")
h3 = TagBase("h3")
h4 = TagBase("h4")
h5 = TagBase("h5")
h6 = TagBase("h6")
hr = TagBase("hr", True)
html = TagBase("html")
i = TagBase("i")
iframe = TagBase("iframe", True)
img = TagBase("img", True)
input_ = TagBase("input", True)
ins = TagBase("ins")
kbd = TagBase("kbd")
label = TagBase("label")
legend = TagBase("legend")
li = TagBase("li")
link = TagBase("link", True)
main = TagBase("main")
mark = TagBase("mark")
marquee = TagBase("marquee")
math = TagBase("math")
menu = TagBase("menu")
menuitem = TagBase("menuitem")
meta = TagBase("meta", True)
meter = TagBase("meter")
nav = TagBase("nav")
object_ = TagBase("object")
noscript = TagBase("noscript")
ol = TagBase("ol")
optgroup = TagBase("optgroup")
option = TagBase("option")
p = TagBase("p")
param = TagBase("param", True)
picture = TagBase("picture")
pre = TagBase("pre")
progress = TagBase("progress")
q = TagBase("q")
rp = TagBase("rp")
rt = TagBase("rt")
ruby = TagBase("ruby")
s = TagBase("s")
samp = TagBase("samp")
script = TagBase("script")
section = TagBase("section")
select = TagBase("select")
small = TagBase("small")
source = TagBase("source", True)
span = TagBase("span")
strike = TagBase("strike")
strong = TagBase("strong")
style = TagBase("style")
sub = TagBase("sub")
summary = TagBase("summary")
sup = TagBase("sup")
svg = TagBase("svg")
table = TagBase("table")
tbody = TagBase("tbody")
template = TagBase("template")
textarea = TagBase("textarea")
td = TagBase("td")
th = TagBase("th")
thead = TagBase("thead")
time = TagBase("time")
title = TagBase("title")
tr = TagBase("tr")
track = TagBase("track", True)
u = TagBase("u")
ul = TagBase("ul")
var = TagBase("var")
video = TagBase("video")
wbr = TagBase("wbr")
