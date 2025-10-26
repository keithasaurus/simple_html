# simple_html

## Why use it?
- clean syntax
- fully-typed
- speed -- faster even than jinja
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
Strings, ints, floats, and Decimals are generally rendered as one would expect expect. For safety, `str`s are 
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

String attributes are escaped by default -- both keys and values. You can use `SafeString` to bypass, if needed.

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

You can also use `int`, `float`, and `Decimal` instances for attribute values.
```python
from decimal import Decimal
from simple_html import div, render, SafeString


render(
    div({"x": 1, "y": 2.3, "z": Decimal('3.45')})    
)
# <div x="1" y="2.3" z="3.45"></div>
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
You can pass many items as a `Tag`'s children using `*args`, lists or generators:
```python
from typing import Generator
from simple_html import div, render, Node, br, p


div(
    *["neat", br], p("cool")
)
# renders to <div>neat<br/><p>cool</p></div>


# passing the raw list instead of *args 
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

### Optimization

#### `prerender`

`prerender` is a very simple function. It just `render`s a `Node` and puts the resulting string inside 
a `SafeString` (so its contents won't be escaped again). It's most useful for prerendering at the module level, 
which ensures the render operation happens only once. A simple use case might be a website's footer:

```python
from simple_html import SafeString, prerender, footer, div, a, head, body, title, h1, html, render


prerendered_footer: SafeString = prerender(
    footer(
        div(a({"href": "/about"}, "About Us")),
        div(a({"href": "/blog"}, "Blog")),
        div(a({"href": "/contact"}, "Contact"))
    )
)


def render_page(page_title: str) -> str:
    return render(
        html(
            head(title(page_title)),
            body(
                h1(page_title),
                prerendered_footer  # this is extremely fast to render
            )
        )
    )
```
This greatly reduces the amount of work `render` needs to do on the prerendered content when outputting HTML.

#### Caching
You may want to cache rendered content. This is easy to do; the main thing to keep in 
mind is you'll likely want to return a `SafeString`. For example, here's how you might cache locally with `lru_cache`:

```python
from simple_html import prerender, SafeString, h1
from functools import lru_cache


@lru_cache
def greeting(name: str) -> SafeString:
    return prerender(
        h1(f"Hello, {name}")
    )
```

One thing to keep in mind is that not all variants of `Node` will work as _arguments_ to a function like the 
one above -- i.e. `list[Node]` is not cacheable. Another way to use `prerender` in combination with a caching function
is to prerender arguments:

```python
from simple_html import prerender, SafeString, h1, div, html, body, head, ul, li
from functools import lru_cache


@lru_cache
def cached_content(children: SafeString) -> SafeString:
    return prerender(
        div(
            h1("This content is cached according to the content of the children"),
            children,
            # presumably this function would have a lot more elements for it to be worth 
            # the caching overhead
        )
    )

def page():
    return html(
        head,
        body(
            cached_content(
                prerender(ul([
                    li(letter) for letter in "abcdefg" 
                ]))
            )
        )
    )
```
