# simple_html
The idea here is to make HTML easy to generate without using templating.
It builds on the idea that HTML is comprised of recursive nodes with a list of 
attributes and a list of child nodes. It's heavily influenced by Elm's Html 
library.
 

Some things nice about this library are:
1. The generated HTML is always valid.
2. Space if always significant.
3. Formalized types mean MyPy can help avoid certain classes of errors.
4. It's framework agnostic.


### Install
`pip install simple_html`

```python
from simple_html.nodes import body, head, html, p
from simple_html.render import render

node = html(
    [],
    head(
        []
    ),
    body(
        [],
        p(
            [("class", "some-class")],
            "Hello World!"
        )
    ),
)

render(node)
```

returns

```html
<html><head></head><body><p class="some-class">Hello World!</p></body></html>
```


Strings are escaped by default, but you can pass in `SafeString`s to avoid escaping.

```python
from simple_html.nodes import br, p, SafeString
from simple_html.render import render

node = p(
    [],
    "Escaped & stuff",
    br([]),
    SafeString("Not escaped & stuff")
)

render(node)
```

returns
```html
<p>Escaped &amp; stuff<br/>Not escaped & stuff</p>
```

For convenience, many tags have been created, but you can create your own as well:

```python
from simple_html.nodes import named_tag
from simple_html.render import render

custom_elem = named_tag("custom-elem")

render(
    custom_elem(
        [("id", "some-custom-elem-id")],
        "Cool"
    )
)
```

renders

```html
<custom-elem id="some-custom-elem-id">Cool</custom-elem>
```

Likewise, some attributes have been created as presets, to help keep data more consistent. 

```python
from simple_html.nodes import div

div(
    [("class", "some-class"),
     ("height", "250")],
    "OK"
)
```

is equivalent to

```python
from simple_html.nodes import div
from simple_html.attributes import class_, height

div(
    [class_("some-class"), height(250)],
    "OK"
)
```

And you can build your own, using `str_attr`, `int_attr`, or `bool_attr`. For instance, here are
several of the attribute preset definitions

```python
checked = bool_attr('checked')
class_ = str_attr('class')
cols = int_attr('cols')
```

#### Status
Very early development. Feel free to contribute.

#### Requirements
Python 3.5+
