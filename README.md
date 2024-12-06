# simple_html

### Template-less. Type-safe. Minified by default. Fast.

simple_html allows you to create HTML in standard Python. Benefits include:
- typically faster than jinja2 -- up to 15x faster
- typically renders fewer bytes than template-based rendering
- types let your editor and tools help you write correct code faster
- lightweight and framework agnostic
- always renders valid html


### Installation
`pip install simple-html`


### Usage

```python
from simple_html import div, h1, render, p

node = div({},
           h1({"id": "hello"},
              "Hello World!"),
           p({},
             "hooray!"))

render(node)  
# <div><h1 id="hello">Hello World!</h1><p>hooray!</p></div> 
```

There are several ways to render nodes:
```python
from simple_html import br, div, h1, img, render

# raw node
render(br)
# <br/>

# node with attributes only
render(img({"src": "/some/image/url.jpg", "alt": "a great picture"}))
# <img src="/some/image/url.jpg" alt="a great picture"/>

# node with children
render(
    div({},
        h1({},
           "something"))
)
# <div><h1>something</h1></div>'
```

TIP: empty attributes can be made less visually busy by using an underscore:
```python
_ = None

render(
    div(_,
        h1(_,
           "something"))
)
# <div><h1>something</h1></div>'
```

Tag attributes with `None` as the value will only render the attribute name:
```python
from simple_html import div, render

render(
    div({"empty-str-attribute": "", 
         "key-only-attr": None})
)
# <div empty-str-attribute="" key-only-attr></div>
```

You can render inline css styles with `render_styles`:
```python
from simple_html import div, render, render_styles

styles = render_styles({"min-width": "25px"})

render(
    div({"style": styles}, 
        "cool")
)
# <div style="min-width:25px;">cool</div>


# ints and floats are legal values
styles = render_styles({"padding": 0, "flex-grow": 0.6})

render(
    div({"style": styles},
        "wow")
)
# <div style="padding:0;flex-grow:0.6;">wow</div>
```


Lists and generators are both valid collections of nodes:
```python
from typing import Generator
from simple_html import div, render, Node, br

_: None = None

def get_list_of_nodes() -> list[Node]:
    return ["neat", br]


render(div(_, get_list_of_nodes()))
# <div>neat<br/></div>


def node_generator() -> Generator[Node, None, None]:
    yield "neat"
    yield br


render(
    div(_, node_generator())
)
# <div>neat<br/></div>
```


For convenience, many tags are provided, but you can also create your own:

```python
from simple_html import Tag, render

custom_elem = Tag("custom-elem")

# works the same as any other tag
node = custom_elem(
    {"id": "some-custom-elem-id"},
    "Wow"
)

render(node)  # <custom-elem id="some-custom-elem-id">Wow</custom-elem>
```


Strings are escaped by default, but you can pass in `SafeString`s to avoid escaping.

```python
from simple_html import br, p, SafeString, render

node = p({},
         "Escaped & stuff",
         br,
         SafeString("Not escaped & stuff"))

render(node)  # <p>Escaped &amp; stuff<br/>Not escaped & stuff</p> 
```

Attributes are also escaped -- both names and values. You can use `SafeString` to bypass, if needed.

```python
from simple_html import div, render, SafeString

escaped_attrs_node = div({"<bad>":"</also bad>"})

render(escaped_attrs_node)  # <div &amp;lt;bad&amp;gt;="&amp;lt;/also bad&amp;gt;"></div>

unescaped_attrs_node = div({SafeString("<bad>"): SafeString("</also bad>")})

render(unescaped_attrs_node)  # <div <bad>="</also bad>"></div>
```
