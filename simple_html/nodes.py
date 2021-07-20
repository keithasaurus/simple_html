from dataclasses import dataclass
from typing import Union, Tuple

from .attributes import Attribute


@dataclass
class SafeString:
    safe_val: str


Node = Union[str, SafeString, "Tag"]


@dataclass
class Tag:
    name: str
    attributes: Tuple[Attribute, ...] = tuple()
    children: Tuple[Node, ...] = tuple()
    self_closes: bool = False

    def __call__(self, *children: Node) -> "Tag":
        return Tag(
            self.name,
            self.attributes,
            children,
            self.self_closes
        )

    def attrs(self,
              *attributes: Attribute,
              **kw_attributes: str) -> "Tag":
        return Tag(
            self.name,
            attributes + tuple(kw_attributes.items()),
            self.children,
            self.self_closes
        )


a = Tag("a")
abbr = Tag("abbr")
address = Tag("address")
area = Tag("area", self_closes=True)
article = Tag("article")
aside = Tag("aside")
audio = Tag("audio")
b = Tag("b")
base = Tag("base", self_closes=True)
bdi = Tag("bdi")
bdo = Tag("bdo")
body = Tag("body")
canvas = Tag("canvas")
blockquote = Tag("blockquote")
br = Tag("br", self_closes=True)
button = Tag("button")
datalist = Tag("datalist")
dd = Tag("dd")
details = Tag("details")
dfn = Tag("dfn")
dl = Tag("dl")
dt = Tag("dt")
caption = Tag("caption")
cite = Tag("cite")
code = Tag("code")
col = Tag("col")
colgroup = Tag("colgroup")
del_ = Tag("del")
div = Tag("div")
em = Tag("em")
embed = Tag("embed", self_closes=True)
fieldset = Tag("fieldset")
figure = Tag("figure")
figcaption = Tag("figcaption")
footer = Tag("footer")
form = Tag("form")
head = Tag("head")
header = Tag("header")
h1 = Tag("h1")
h2 = Tag("h2")
h3 = Tag("h3")
h4 = Tag("h4")
h5 = Tag("h5")
h6 = Tag("h6")
hr = Tag("hr", self_closes=True)
html = Tag("html")
i = Tag("i")
iframe = Tag("iframe", self_closes=True)
img = Tag("img", self_closes=True)
input_ = Tag("input", self_closes=True)
ins = Tag("ins")
kbd = Tag("kbd")
label = Tag("label")
legend = Tag("legend")
li = Tag("li")
link = Tag("link", self_closes=True)
main = Tag("main")
mark = Tag("mark")
math = Tag("math")
menu = Tag("menu")
menuitem = Tag("menuitem")
meta = Tag("meta", self_closes=True)
meter = Tag("meter")
nav = Tag("nav")
object_ = Tag("object")
noscript = Tag("noscript")
ol = Tag("ol")
optgroup = Tag("optgroup")
option = Tag("option")
p = Tag("p")
param = Tag("param", self_closes=True)
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
source = Tag("source", self_closes=True)
span = Tag("span")
strong = Tag("strong")
style = Tag("style")
sub = Tag("sub")
summary = Tag("summary")
sup = Tag("sup")
table = Tag("table")
tbody = Tag("tbody")
thead = Tag("thead")
textarea = Tag("textarea")
td = Tag("td")
th = Tag("th")
time = Tag("time")
title = Tag("title")
tr = Tag("tr")
track = Tag("track", self_closes=True)
u = Tag("u")
ul = Tag("ul")
var = Tag("var")
video = Tag("video")
wbr = Tag("wbr")
