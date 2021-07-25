# simple_html

### Template-less. Type-safe. Minified by default.

simple_html is built to simplify HTML rendering in Python. No templates needed. Just create HTML in 
normal Python. In most cases, the code will be more concise than standard HTML. Other benefits include:
- typically renders fewer bytes than template-based rendering
- types mean your editor and tools can help you write correct code faster
- no framework needed
- lightweight


### Installation
`pip install simple_html`


### Usage
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

render(node)  # returns: <html><head></head><body><p id="hello">Hello World!</p></body></html> 
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

render(node)  # returns: <p>Escaped &amp; stuff<br/>Not escaped & stuff</p> 
```

For convenience, many tags are provided, but you can create your own as well:

```python
from simple_html.nodes import TagBase 
from simple_html.render import render

custom_elem = TagBase("custom-elem")

render(
    custom_elem.attrs(id="some-custom-elem-id")(
        "Wow"
    )
)  # returns: <custom-elem id="some-custom-elem-id">Wow</custom-elem> 
```

Likewise, some attributes have been created as type-safe presets. Note that there are multiple ways to create attributes. 
The examples below are all equivalent:

```python
from simple_html.attributes import height, id_
from simple_html.nodes import div


# **kwargs: recommended for most cases
div.attrs(id="some-id", height="100")

# *args: useful for attributes that may be reserved keywords or when type constraints are desired.
# Presets, raw tuples, and kwargs can be used interchangeably.
div.attrs(("id", "some-id"), ("height", "100"))

div.attrs(("id", "some-id"), height(100))

div.attrs(id_("some-id"), height(100))

div.attrs(id_("some-id"), height="100")

# each would render to: <div id="some-id" height="100"></div> 
```

You can build your own presets, using `str_attr`, `int_attr`, or `bool_attr`. For instance, here are
several of the attribute preset definitions

```python
from simple_html.attributes import bool_attr, int_attr, str_attr

checked = bool_attr('checked')
class_ = str_attr('class')
cols = int_attr('cols')
```
But anything that renders to the type of `Attribute` will work.