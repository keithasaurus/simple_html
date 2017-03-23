from .attributes import Attribute
from typing import Any, Callable, List, NamedTuple, Tuple


class SafeString(NamedTuple):
    safe_val: str


class Tag(NamedTuple):
    name: str
    attrs: List[Attribute]
    nodes: Tuple[Any, ...]  # really Tuple[Union["Tag", SafeString, str], ...]


def named_tag(tag_name: str) -> Callable:
    def closure(attrs: List[Attribute], *nodes) -> Tag:
        return Tag(
            tag_name,
            attrs,
            nodes
        )

    return closure


a = named_tag('a')
abbr = named_tag('abbr')
address = named_tag('address')
article = named_tag('article')
aside = named_tag('aside')
audio = named_tag('audio')
b = named_tag('b')
bdi = named_tag('bdi')
bdo = named_tag('bdo')
body = named_tag('body')
canvas = named_tag('canvas')
blockquote = named_tag('blockquote')
br = named_tag('br')
button = named_tag('button')
datalist = named_tag('datalist')
dd = named_tag('dd')
details = named_tag('details')
dfn = named_tag('dfn')
dl = named_tag('dl')
dt = named_tag('dt')
caption = named_tag('caption')
cite = named_tag('cite')
code = named_tag('code')
col = named_tag('col')
colgroup = named_tag('colgroup')
del_ = named_tag('del')
div = named_tag('div')
em = named_tag('em')
embed = named_tag('embed')
fieldset = named_tag('fieldset')
figure = named_tag('figure')
figcaption = named_tag('figcaption')
footer = named_tag('footer')
form = named_tag('form')
head = named_tag('head')
header = named_tag('header')
h1 = named_tag('h1')
h2 = named_tag('h2')
h3 = named_tag('h3')
h4 = named_tag('h4')
h5 = named_tag('h5')
h6 = named_tag('h6')
hr = named_tag('hr')
html = named_tag('html')
i = named_tag('i')
iframe = named_tag('iframe')
img = named_tag('img')
input_ = named_tag('input')
ins = named_tag('ins')
kbd = named_tag('kbd')
label = named_tag('label')
legend = named_tag('legend')
li = named_tag('li')
main = named_tag('main')
mark = named_tag('mark')
math = named_tag('math')
menu = named_tag('menu')
menuitem = named_tag('menuitem')
meta = named_tag('meta')
meter = named_tag('meter')
nav = named_tag('nav')
object_ = named_tag('object')
ol = named_tag('ol')
optgroup = named_tag('optgroup')
option = named_tag('option')
p = named_tag('p')
param = named_tag('param')
pre = named_tag('pre')
progress = named_tag('progress')
q = named_tag('q')
rp = named_tag('rp')
rt = named_tag('rt')
ruby = named_tag('ruby')
s = named_tag('s')
samp = named_tag('samp')
script = named_tag('script')
section = named_tag('section')
select = named_tag('select')
small = named_tag('small')
source = named_tag('source')
span = named_tag('span')
strong = named_tag('strong')
style = named_tag('style')
sub = named_tag('sub')
summary = named_tag('summary')
sup = named_tag('sup')
table = named_tag('table')
tbody = named_tag('tbody')
thead = named_tag('thead')
textarea = named_tag('textarea')
td = named_tag('td')
th = named_tag('th')
time = named_tag('time')
tr = named_tag('tr')
track = named_tag('track')
u = named_tag('u')
ul = named_tag('ul')
var = named_tag('var')
video = named_tag('video')
wbr = named_tag('wbr')


