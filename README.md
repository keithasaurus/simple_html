# simple_html

### Template-less. Type-safe. Minified by default. Fast.

simple_html allows you to create HTML in standard Python. Benefits include:
- it's typically faster than jinja2 -- up to 20x faster
- it typically renders fewer bytes than template-based rendering
- types mean your editor and tools can help you write correct code faster
- lightweight and framework agnostic 


### Installation
`pip install simple-html`


### Usage

```python
from simple_html import div, h1, render

node = div({},
           h1({"id": "hello"},
              "Hello World!"
              )
           )

render(node)  
# <div><h1 id="hello">Hello World!</h1></div> 
```

There are several ways to render nodes:
```python
from simple_html import br, div, h1, img, render, span

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

Node attributes with `None` as the value will only render the key
```python
from simple_html import div, render

render(div({"empty-str-attribute": "", "key-only-attr": None}))
# <div empty-str-attribute="" key-only-attr></div>
```

Strings are escaped by default, but you can pass in `SafeString`s to avoid escaping.

```python
from simple_html import br, p, safe_string, render

node = p({},
         "Escaped & stuff",
         br,
         safe_string("Not escaped & stuff")
         )

render(node)  # returns: <p>Escaped &amp; stuff<br/>Not escaped & stuff</p> 
```

Lists and generators are both valid collections of nodes:
```python
from typing import Generator
from simple_html import div, render, Node, br


def list_of_nodes_function() -> list[Node]:
    return ["neat", br]


render(div({}, list_of_nodes_function()))
# <div>neat<br/></div>


def node_generator() -> Generator[Node, None, None]:
    yield "neat"
    yield br


render(div({}, node_generator()))
# <div>neat<br/></div>
```


For convenience, many tags are provided, but you can create your own as well:

```python
from simple_html import Tag, render

custom_elem = Tag("custom-elem")

render(
    custom_elem({"id": "some-custom-elem-id"},
                "Wow"
                )
)  # returns: <custom-elem id="some-custom-elem-id">Wow</custom-elem> 
```

Likewise, some attributes have been created as type-safe presets. Note that there are multiple ways to create attributes. 