# simple_html
The idea here is make sure HTML is easy to generate but always valid. It
builds on the idea that HTML is comprised of recursive nodes with a list of 
attributes and a list of child nodes.

```python
from simple_html.nodes import body, head, html, p
from simple_html.render import render_node

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

render_node(node)
```

returns

```html
<html><head/><body><p class="some-class">Hello World!</p></body></html>
```


Strings are escaped by default, but you can pass in `SafeString`s to avoid escaping.
```python
from simple_html.nodes import br, p, SafeString
from simple_html.render import render_node

node = p(
    [],
    "Escaped & stuff",
    br([]),
    SafeString("Not escaped & stuff")
) 

render_node(node)
```

returns
```html
<p>Escaped &amp; stuff<br/>Not escaped & stuff</p>
```

For convenience, many tags have been created, but you can create your own as well:
```python
from simple_html.nodes import named_tag
from simple_html.render import render_node

custom_elem = named_tag("custom-elem")

render_node(
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
Python 3.6+
