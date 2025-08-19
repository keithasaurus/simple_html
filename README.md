# simple_html

## Why use it?
- clean syntax
- fully-typed
- speed -- faster even than jinja2
- zero dependencies
- escaped by default
- usually renders fewer bytes than templating


## Installation
`pip install simple-html`


## Usage

```python
from simple_html import h1, render

node = h1("Hello World!")

render(node)  
# <h1>Hello World!</h1> 
```

To add attributes to a tag, pass a dictionary as the first argument: 
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
from simple_html import br, div, h1, img, span, render

# raw node renders to empty tag
render(br)
# <br/>

# node with attributes but no children
render(
    img({"src": "/some-image.jpg", "alt": "a great picture"})
)
# <img src="/some-image.jpg" alt="a great picture"/>

# nodes with children and (optional) attributes
render(
    div(
        h1({"class": "neat-class"}, 
        span("cool"),
        br)
    )
)
# <div><h1 class="neat-class"><span>cool</span><br/></h1></div>
```
### Strings and Things
Strings, ints, floats, and Decimals are generally rendered as you'd expect. The main thing know is that `str`s are 
escaped by default; `SafeString`s can be used to bypass escaping.

```python
from simple_html import br, p, SafeString, render

node = p("Escaped & stuff",
         br,
         SafeString("Not escaped & stuff"))

render(node)  
# <p>Escaped &amp; stuff<br/>Not escaped & stuff</p> 
```

### Attributes

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

render(
    div({"<bad>":"</also bad>"})
)
# <div &amp;lt;bad&amp;gt;="&amp;lt;/also bad&amp;gt;"></div>

render(
    div({SafeString("<bad>"): SafeString("</also bad>")})
)  
# <div <bad>="</also bad>"></div>
```

### CSS

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

### Collections
You can pass many items as a `Tag`'s children using `*args`, lists and generators:
```python
from typing import Generator
from simple_html import div, render, Node, br, p

div(
    *["neat", br], p("cool")
)
# renders to <div>neat<br/><p>cool</p></div>

# same, but no star args
div(
    ["neat", br],
    p("cool")
)
# renders to <div>neat<br/><p>cool</p></div>


def node_generator() -> Generator[Node, None, None]:
    yield "neat"
    yield br 


div(node_generator(), p("cool"))
# renders to <div>neat<br/><p>cool</p></div>
```

#### Custom Tags

For convenience, most common tags are provided, but you can also create your own:

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
