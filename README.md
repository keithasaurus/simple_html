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
from simple_html import h1, render

node = h1("Hello World!")

render(node)  
# <h1>Hello World!</h1> 
```
Here, `h1` is a `Tag` and the string "Hello World!" is it's only child. We call `render` to produce a string.

There are several ways to use `Tag`s:
```python
from simple_html import br, div, h1, img

# raw node
br
# renders to <br/>

# node with attributes only
img({"src": "/some-image.jpg", "alt": "a great picture"})
# renders to <img src="/some-image.jpg" alt="a great picture"/>

# node with children and (optional) attributes
div(
    h1({"class": "neat-class"}, 
       "cool")
)
# renders to <div><h1 class="neat-class">cool</h1></div>'
```

#### Working with Attributes

Tag attributes with `None` as the value will only render the attribute name:
```python
from simple_html import div, render

node = div({"empty-str-attribute": "", 
            "key-only-attr": None})
render(node)
# <div empty-str-attribute="" key-only-attr></div>
```

You can render inline css styles with `render_styles`:
```python
from simple_html import div, render, render_styles

styles = render_styles({"min-width": "25px"})

node = div({"style": styles}, "cool")

render(node)
# <div style="min-width:25px;">cool</div>


# ints and floats are legal values
styles = render_styles({"padding": 0, "flex-grow": 0.6})

node = div({"style": styles}, "wow")

render(node)
# <div style="padding:0;flex-grow:0.6;">wow</div>
```

Attributes are escaped by default -- both names and values. You can use `SafeString` to bypass, if needed.

```python
from simple_html import div, render, SafeString

escaped_attrs_node = div({"<bad>":"</also bad>"})

render(escaped_attrs_node)  # <div &amp;lt;bad&amp;gt;="&amp;lt;/also bad&amp;gt;"></div>

unescaped_attrs_node = div({SafeString("<bad>"): SafeString("</also bad>")})

render(unescaped_attrs_node)  # <div <bad>="</also bad>"></div>
```


#### The `Node` type

The type for `Node` is fairly flexible:
```python
from typing import Union, Generator
from simple_html import SafeString

Node = Union[
    str,
    SafeString, 
    list["Node"],
    Generator["Node", None, None],
    # You probably won't need to think about these two much, since they are mainly internal to the library
    "Tag", 
    "TagTuple",
]
```

`str`s are escaped by default, but you can pass in `SafeString`s to avoid escaping.

```python
from simple_html import br, p, SafeString, render

node = p("Escaped & stuff",
         br,
         SafeString("Not escaped & stuff"))

render(node)  # <p>Escaped &amp; stuff<br/>Not escaped & stuff</p> 
```

Lists and generators are both valid collections of nodes:
```python
from typing import Generator
from simple_html import div, render, Node, br


def get_list_of_nodes() -> list[Node]:
    return ["neat", br]


render(div(get_list_of_nodes()))
# <div>neat<br/></div>


def node_generator() -> Generator[Node, None, None]:
    yield "neat"
    yield br


render(
    div(node_generator())
)
# <div>neat<br/></div>
```

#### Custom Tags

For convenience, many tags are provided, but you can also create your own:

```python
from simple_html import Tag, render

custom_elem = Tag("custom-elem")

# works the same as any other tag
node = custom_elem(
    {"id": "some-custom-elem-id"},
    "Wow"
)

render(node)
# <custom-elem id="some-custom-elem-id">Wow</custom-elem>
```
