from typing import Callable, List, Tuple

Attribute = Tuple[str, str]


def bool_attr(name: str) -> Attribute:
    """
    e.g. required="required", selected="selected"
    """
    return name, name


def int_attr(name: str) -> Callable[[int], Attribute]:
    def closure(val: int) -> Attribute:
        return name, str(val)
    return closure


def str_attr(name: str) -> Callable[[str], Attribute]:
    def closure(val: str) -> Attribute:
        return name, val

    return closure


def style(props: List[Tuple[str, str]]) -> Attribute:
    return "style", " ".join([f"{key}: {val};" for key, val in props])


alt = str_attr('alt')
accept = str_attr('accept')
accept_charset = str_attr('acceptCharset')
action = str_attr('action')
autocomplete = str_attr('autocomplete')
autofocus = bool_attr('autofocus')
checked = bool_attr('checked')
class_ = str_attr('class')
cols = int_attr('cols')
default_value = str_attr('defaultValue')
disabled = bool_attr('disabled')
enctype = str_attr('enctype')
for_ = str_attr('for')
form = str_attr('form')
formaction = str_attr('formaction')
height = int_attr('height')
href = str_attr('href')
id = str_attr('id')
max = str_attr('max')
maxlength = int_attr('maxlength')
method = str_attr('method')
min = str_attr('min')
minlength = int_attr('minlength')
multiple = bool_attr('multiple')
name = str_attr('name')
novalidate = bool_attr('novalidate')
pattern = str_attr('patter')
placeholder = str_attr('placeholder')
readonly = bool_attr('readonly')
rows = str_attr('rows')
selected = bool_attr('selected')
size = int_attr('size')
src = str_attr('src')
step = str_attr('step')
target = str_attr('target')
title = str_attr('title')
type_ = str_attr('type')
value = str_attr('value')
width = int_attr('width')
wrap = str_attr('wrap')
