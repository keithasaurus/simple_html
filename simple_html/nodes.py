from dataclasses import dataclass
from typing import Union, Tuple

from .attributes import Attribute


@dataclass
class SafeString:
    safe_val: str


Node = Union[str, SafeString, "Tag", "TagBase"]


class Tag:
    """
    Not a dataclass, nor immutable because of observed
    performance increase. The recommended means of using
    this class results in not mutating objects in any case.
    """
    def __init__(self,
                 tag_base: "TagBase",
                 attributes: Tuple[Attribute, ...] = tuple(),
                 children: Tuple[Node, ...] = tuple()
                 ) -> None:
        self.tag_base = tag_base
        self.attributes = attributes
        self.children = children

    def __call__(self, *children: Node) -> "Tag":
        return Tag(tag_base=self.tag_base,
                   attributes=self.attributes,
                   children=children)

    def attrs(self,
              *attributes: Attribute,
              **kw_attributes: str) -> "Tag":
        return Tag(tag_base=self.tag_base,
                   attributes=attributes + tuple(kw_attributes.items()),
                   children=self.children)


@dataclass(frozen=True)
class TagBase:
    name: str
    self_closes: bool = False

    def __call__(self, *children: Node) -> Tag:
        return Tag(tag_base=self,
                   children=children)

    def attrs(self,
              *attributes: Attribute,
              **kw_attributes: str
              ) -> Tag:
        return Tag(tag_base=self,
                   attributes=attributes + tuple(kw_attributes.items()))


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
body = TagBase("body")
canvas = TagBase("canvas")
blockquote = TagBase("blockquote")
br = TagBase("br", True)
button = TagBase("button")
datalist = TagBase("datalist")
dd = TagBase("dd")
details = TagBase("details")
dfn = TagBase("dfn")
dl = TagBase("dl")
dt = TagBase("dt")
caption = TagBase("caption")
cite = TagBase("cite")
code = TagBase("code")
col = TagBase("col")
colgroup = TagBase("colgroup")
del_ = TagBase("del")
div = TagBase("div")
em = TagBase("em")
embed = TagBase("embed", True)
fieldset = TagBase("fieldset")
figure = TagBase("figure")
figcaption = TagBase("figcaption")
footer = TagBase("footer")
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
strong = TagBase("strong")
style = TagBase("style")
sub = TagBase("sub")
summary = TagBase("summary")
sup = TagBase("sup")
table = TagBase("table")
tbody = TagBase("tbody")
thead = TagBase("thead")
textarea = TagBase("textarea")
td = TagBase("td")
th = TagBase("th")
time = TagBase("time")
title = TagBase("title")
tr = TagBase("tr")
track = TagBase("track", True)
u = TagBase("u")
ul = TagBase("ul")
var = TagBase("var")
video = TagBase("video")
wbr = TagBase("wbr")
