# simple_html

Template-less html in Python.

### Type-safe. Minified by default. Fast.

simple_html is built to simplify html rendering in Python. No templates needed. Just create html in 
normal Python. In most cases, the code will be more concise than standard html. Other benefits include:
- typically renders fewer bytes than template-based rendering
- types mean your editor and tools can help you write correct code faster
- no framework needed


### Install
`pip install simple_html`

```python
from simple_html.nodes import body, head, html, p
from simple_html.render import render

node = html(
    head,
    body(
        p.attrs(id="hello")( 
            "Hello World!"
        )
    )
)

render(node)
```

returns

```html
<html><head></head><body><p id="hello">Hello World!</p></body></html>
```


Strings are escaped by default, but you can pass in `SafeString`s to avoid escaping.

```python
from simple_html.nodes import br, p, SafeString
from simple_html.render import render

node = p(
    "Escaped & stuff",
    br,
    SafeString("Not escaped & stuff")
)

render(node)
```

returns
```html
<p>Escaped &amp; stuff<br/>Not escaped & stuff</p>
```

For convenience, many tags are provided, but you can create your own as well:

```python
from simple_html.nodes import TagBase 
from simple_html.render import render

custom_elem = TagBase("custom-elem")

render(
    custom_elem.attrs(id="some-custom-elem-id")(
        "Cool"
    )
)
```

renders

```html
<custom-elem id="some-custom-elem-id">Cool</custom-elem>
```

Likewise, some attributes have been created as type-safe presets. Note that there are multiple ways to create attributes. 
The examples below are equivalent:

```python
from simple_html.attributes import height, id_
from simple_html.nodes import div


# **kwargs: recommended for most cases
div.attrs(id="some-id", height="100")

# *args: useful for attributes that may be reserved keywords, when type constraints are desired, 
# or when multiple of the same attribute are needed. Presets and raw tuples can be used interchangeably. 
div.attrs(("id", "some-id"), height(100))
div.attrs(id_("some-id"), height(100))
div.attrs(("id", "some-id"), ("height", "100"))
```

You can build your own presets, using `str_attr`, `int_attr`, or `bool_attr`. For instance, here are
several of the attribute preset definitions

```python
from simple_html.attributes import bool_attr, int_attr, str_attr
checked = bool_attr('checked')
class_ = str_attr('class')
cols = int_attr('cols')
```
