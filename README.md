# simple_html

### Why should I use it?
- clean syntax
- fully-typed
- always renders valid html
- speed -- faster than jinja2  
- zero dependencies
- framework agnostic
- escaped by default
- space significance typically results in fewer bytes rendered


### Installation
`pip install simple-html`


### Usage

```python
from simple_html import h1, render

node = h1("Hello World!")

render(node)  
# <h1>Hello World!</h1> 
```

If you want a tag to have attribute, you can pass a dictionary as the first argument: 
```python
node = h1({"id": "heading"}, "Hello World!")

render(node)  
# <h1 id="heading">Hello World!</h1> 
```

Here's a fuller-featured example:
```python
from simple_html import render, DOCTYPE_HTML5, html, head, title, body, h1, div, p, br, ul, li

render(
    DOCTYPE_HTML5,
    html(
        head(
            title("A Great Webpage!")
        ),
        body(
            h1({"class": "great header"},
               "Welcome!"),
            div(
                p("This webpage is great for three reasons:"),
                ul(li(f"{s} reason") for s in ["first", "second", "third"]),
            ),
            br,
            "Hope you like it!"
        )
    )
)

```
The above renders to a minified version of the following html:
```html
<!doctype html>
<html>
<head><title>A Great Webpage!</title></head>
<body><h1 class="great header">Welcome!</h1>
<div><p>This webpage is great for three reasons:</p>
    <ul>
        <li>first reason</li>
        <li>second reason</li>
        <li>third reason</li>
    </ul>
</div>
<br/>Hope you like it!
</body>
</html>
```

As you might have noticed, there are several ways to use `Tag`s:
```python
from simple_html import br, div, h1, img, span

# raw node renders to empty tag
br
# <br/>

# node with attributes but not children
img({"src": "/some-image.jpg", "alt": "a great picture"})
# <img src="/some-image.jpg" alt="a great picture"/>

# nodes with children and (optional) attributes
div(
    h1({"class": "neat-class"}, 
       span("cool"),
       br)
)
# <div><h1 class="neat-class"><span>cool</span><br/></h1></div>
```

#### More About Attributes

Tag attributes are defined as simple dictionaries -- typically you'll just use strings for both keys and values. Note 
that Tag attributes with `None` as the value will only render the attribute name:
```python
from simple_html import div, render

node = div({"empty-str-attribute": "", 
            "key-only-attr": None})

render(node)
# <div empty-str-attribute="" key-only-attr></div>
```

Attributes are escaped by default -- both keys and values. You can use `SafeString` to bypass, if needed.

```python
from simple_html import div, render, SafeString

escaped_attrs_node = div({"<bad>":"</also bad>"})

render(escaped_attrs_node)  # <div &amp;lt;bad&amp;gt;="&amp;lt;/also bad&amp;gt;"></div>

unescaped_attrs_node = div({SafeString("<bad>"): SafeString("</also bad>")})

render(unescaped_attrs_node)  # <div <bad>="</also bad>"></div>
```

#### CSS

You can render inline CSS styles with `render_styles`:
```python
from simple_html import div, render, render_styles

styles = render_styles({"min-width": "25px"})

node = div({"style": styles}, "cool")

render(node)
# <div style="min-width:25px;">cool</div>


# ints, floats, and Decimals are legal values
styles = render_styles({"padding": 0, "flex-grow": 0.6})

node = div({"style": styles}, "wow")

render(node)
# <div style="padding:0;flex-grow:0.6;">wow</div>
```

#### The `Node` type

`Node` defines what types of objects can be used as `Tag` `children`, or passed as arguments to `render`:

```python
from decimal import Decimal
from typing import Union, Generator
from simple_html import SafeString

Node = Union[
    str,
    SafeString, 
    float,
    int,
    Decimal,
    list["Node"],
    Generator["Node", None, None],
    # You probably won't need to think about these two much, since they are mainly internal to the library
    "Tag", 
    "TagTuple",
]
```
While `Tag` and `TagTuple` are amongst the most common types in simple_html, it's not common to work directly with them; instead developers
should expect to use objects like `div`, `a`, `span`, etc., which use these types transparently. 

Some things to note:

- `str`s are escaped by default, but you can pass in `SafeString`s to avoid escaping.
    ```python
    from simple_html import br, p, SafeString, render

    node = p("Escaped & stuff",
             br,
             SafeString("Not escaped & stuff"))

    render(node)  # <p>Escaped &amp; stuff<br/>Not escaped & stuff</p> 
    ```

- lists and generators are both valid collections of nodes:
    ```python
    from typing import Generator
    from simple_html import div, render, Node, br

  
    div(["neat", br])
    # renders to <div>neat<br/></div>


    def node_generator() -> Generator[Node, None, None]:
        yield "neat"
        yield br


    div(node_generator())
    # renders to <div>neat<br/></div>
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
