from typing import Callable, List, Tuple, Optional

Attribute = Tuple[str, Optional[str]]


def bool_attr(attr_name: str) -> Attribute:
    """
    e.g. required="required", selected="selected"
    """
    return attr_name, attr_name


def int_attr(attr_name: str) -> Callable[[int], Attribute]:
    def closure(val: int) -> Attribute:
        return attr_name, str(val)

    return closure


def str_attr(attr_name: str) -> Callable[[str], Attribute]:
    def closure(val: str) -> Attribute:
        return attr_name, val

    return closure


def style(props: List[Tuple[str, str]]) -> Attribute:
    return "style", " ".join([f"{key}: {val};" for key, val in props])


def no_value(attr_name: str) -> Attribute:
    return attr_name, None


alt = str_attr("alt")
accept = str_attr("accept")
accept_charset = str_attr("acceptCharset")
accesskey = str_attr("accesskey")
action = str_attr("action")
align = str_attr("align")
async_ = bool_attr("async")
autocomplete = str_attr("autocomplete")
autofocus = bool_attr("autofocus")
autoplay = bool_attr("autoplay")
challenge = str_attr("challenge")
charset = str_attr("charset")
checked = bool_attr("checked")
cite = str_attr("cite")
class_ = str_attr("class")
cols = int_attr("cols")
colspan = int_attr("colspan")
content = str_attr("content")
content_editable = bool_attr("contentEditable")
contextmenu = str_attr("contextmenu")
controls = bool_attr("controls")
coords = str_attr("coords")
datetime_ = str_attr("datetime")
default = bool_attr("default")
default_value = str_attr("defaultValue")
defer = bool_attr("defer")
dir_ = str_attr("dir")
disabled = bool_attr("disabled")
download = bool_attr("download")
download_as = str_attr("download")
draggable = str_attr("draggable")
dropzone = str_attr("dropzone")
enctype = str_attr("enctype")
for_ = str_attr("for")
form = str_attr("form")
formaction = str_attr("formaction")
headers = str_attr("headers")
height = int_attr("height")
hidden = bool_attr("hidden")
href = str_attr("href")
href_lang = str_attr("hreflang")
http_equiv = str_attr("httpEquiv")
id_ = str_attr("id")
is_map = bool_attr("isMap")
itemprop = str_attr("itemprop")
itemscope = str_attr("itemscope")
itemtype = str_attr("itemtype")
keytype = str_attr("keytype")
kind = str_attr("kind")
lang = str_attr("lang")
language = str_attr("language")
loop = bool_attr("loop")
manifest = str_attr("manifest")
max_ = str_attr("max")
maxlength = int_attr("maxlength")
media = str_attr("media")
method = str_attr("method")
min_ = str_attr("min")
minlength = int_attr("minlength")
multiple = bool_attr("multiple")
name = str_attr("name")
novalidate = bool_attr("novalidate")
pattern = str_attr("pattern")
ping = str_attr("ping")
placeholder = str_attr("placeholder")
poster = str_attr("poster")
preload = str_attr("preload")
pubdate = str_attr("pubdate")
readonly = bool_attr("readonly")
rel = str_attr("rel")
reversed_ = bool_attr("reversed")
rows = str_attr("rows")
rowspan = int_attr("rowspan")
sandbox = str_attr("sandbox")
scope = str_attr("scope")
scoped = bool_attr("scoped")
seamless = bool_attr("seamless")
selected = bool_attr("selected")
shape = str_attr("shape")
size = int_attr("size")
sizes = str_attr("sizes")
spellcheck = bool_attr("spellcheck")
src = str_attr("src")
srcdoc = str_attr("srcdoc")
srclang = str_attr("srclang")
start = int_attr("start")
step = str_attr("step")
tab_index = int_attr("tabIndex")
target = str_attr("target")
title = str_attr("title")
type_ = str_attr("type")
use_map = str_attr("useMap")
value = str_attr("value")
width = int_attr("width")
wrap = str_attr("wrap")
xml_lang = str_attr("xml:lang")
xmlns = str_attr("xmlns")

# events
onblur = str_attr("onblur")
onclick = str_attr("onclick")
oncheck = str_attr("oncheck")
onchange = str_attr("onchange")
onfocus = str_attr("onfocus")
oninput = str_attr("oninput")
onmouseover = str_attr("onmouseover")
onmouseenter = str_attr("onmouseenter")
onmouseleave = str_attr("onmouseleave")
onsubmit = str_attr("onsubmit")
