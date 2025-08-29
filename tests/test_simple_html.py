import json
from decimal import Decimal
from typing import Generator

from simple_html import (
    SafeString,
    a,
    body,
    br,
    button,
    div,
    form,
    head,
    html,
    input_,
    label,
    p,
    script,
    span,
    Node,
    DOCTYPE_HTML5,
    render,
    render_styles,
    img, title, h1,
)
from simple_html.utils import escape_attribute_key, templatize


def test_renders_no_children() -> None:
    node = a

    assert render(node) == "<a></a>"


def test_renders_children() -> None:
    node = p(
        {"class": "pclass"},
        "hey!",
        a(
            {"href": "https://google.com", "class": "aclass"},
            "link text",
            span({}, "whatever"),
        ),
        br,
    )

    assert render(node) == (
        '<p class="pclass">hey!<a href="https://google.com" '
        'class="aclass">link text<span>whatever</span></a>'
        "<br/></p>"
    )


def test_hello_world() -> None:
    node = html({}, head, body({}, p({"class": "some-class"}, "Hello World!")))

    assert render(node) == (
        '<html><head></head><body><p class="some-class">Hello World!</p>'
        "</body></html>"
    )


def test_string_attrs_work_as_expected() -> None:
    node = div({"class": "dinosaur", "some-random-attr": "spam"})
    assert render(node) == '<div class="dinosaur" some-random-attr="spam"></div>'


def test_escapes_normal_strings() -> None:
    node = "some < string"

    assert render(node) == "some &lt; string"


def test_safe_strings_are_not_escaped() -> None:
    assert render(SafeString("some < string")) == "some < string"


def test_simple_form() -> None:
    node = form(
        {"method": "POST", "enctype": "multipart/form-data"},
        label(
            {},
            "Name",
            input_(
                {"type": "text", "value": "some_value", "placeholder": "example text"}
            ),
        ),
        div({"class": "button-container"}, button({}, "Submit")),
    )

    assert render(node) == (
        '<form method="POST" enctype="multipart/form-data">'
        "<label>Name"
        '<input type="text" value="some_value" placeholder="example text"/>'
        "</label>"
        '<div class="button-container">'
        "<button>Submit</button>"
        "</div>"
        "</form>"
    )


def test_safestring_in_tag() -> None:
    node = script({"type": "ld+json"}, SafeString(json.dumps({"some_key": "some_val"})))

    assert render(node) == ('<script type="ld+json">{"some_key": "some_val"}</script>')


def test_script_tag_doesnt_self_close() -> None:
    example_script_url = "https://example.com/main.js"

    node = script({"src": example_script_url})
    assert render(node) == f'<script src="{example_script_url}"></script>'


def test_kw_attributes() -> None:
    node = div({"class": "first", "name": "some_name", "style": "color:blue;"}, "okok")

    assert (
        render(node)
        == '<div class="first" name="some_name" style="color:blue;">okok</div>'
    )


def test_uncalled_tag_renders() -> None:
    assert render(a) == "<a></a>"
    assert render(br) == "<br/>"


def test_attribute_without_value_rendered_as_expected() -> None:
    assert render(a({"something": ""})) == '<a something=""></a>'
    assert render(a({"something": None})) == "<a something></a>"


def test_self_closing_still_nests_children() -> None:
    assert render(img({}, div)) == "<img><div></div></img>"
    assert render(img({"id": "4"}, div)) == '<img id="4"><div></div></img>'


def test_render_with_doctype() -> None:
    assert render(DOCTYPE_HTML5, html) == "<!doctype html><html></html>"


def test_render_list() -> None:
    assert render([br, "ok", div({}, "great")]) == "<br/>ok<div>great</div>"

    assert render([]) == ""


def test_render_generator() -> None:
    assert render(div for _ in range(2)) == "<div></div><div></div>"

    def some_func() -> Generator[Node, None, None]:
        yield ["abc", br]
        yield "123"

    assert render(some_func()) == "abc<br/>123"


def test_render_kw_attribute_with_none() -> None:
    assert render(script({"defer": ""})) == '<script defer=""></script>'


def test_can_render_empty() -> None:
    assert render([]) == ""
    assert (
        render(div({}, [], "hello ", [], span({}, "World!"), []))
        == "<div>hello <span>World!</span></div>"
    )


def test_hash_for_safestring() -> None:
    assert hash(SafeString("okokok")) == hash(("SafeString", "okokok"))


def test_escape_key() -> None:
    assert escape_attribute_key("") == ""
    assert escape_attribute_key(">") == "&gt;"
    assert escape_attribute_key("<") == "&lt;"
    assert escape_attribute_key('"') == "&quot;"
    assert escape_attribute_key("\\") == "&#x5C;"
    assert escape_attribute_key("'") == "&#x27;"
    assert escape_attribute_key("=") == "&#x3D;"
    assert escape_attribute_key("`") == "&#x60;"
    assert (
        escape_attribute_key("something with spaces")
        == "something&nbsp;with&nbsp;spaces"
    )


def test_render_with_escaped_attributes() -> None:
    assert (
        render(div({'onmousenter="alert(1)" noop': "1"}))
        == '<div onmousenter&#x3D;&quot;alert(1)&quot;&nbsp;noop="1"></div>'
    )
    assert (
        render(span({'<script>"</script>': '">'}))
        == '<span &lt;script&gt;&quot;&lt;/script&gt;="&quot;&gt;"></span>'
    )
    # vals and keys escape slightly differently
    assert (
        render(div({'onmousenter="alert(1)" noop': 'onmousenter="alert(1)" noop'}))
        == '<div onmousenter&#x3D;&quot;alert(1)&quot;&nbsp;noop="onmousenter=&quot;alert(1)&quot; noop"></div>'
    )


def test_render_with_safestring_attributes() -> None:
    bad_key = 'onmousenter="alert(1)" noop'
    bad_val = "<script></script>"
    assert (
        render(div({SafeString(bad_key): SafeString(bad_val)}))
        == f'<div {bad_key}="{bad_val}"></div>'
    )


def test_safestring_repr() -> None:
    assert repr(SafeString("abc123")) == "SafeString(safe_str='abc123')"


def test_safe_string_eq() -> None:
    assert "abc123" != SafeString("abc123")
    assert SafeString("a") != SafeString("abc123")
    assert SafeString("abc123") == SafeString("abc123")



def test_render_styles() -> None:
    assert render_styles({}) == SafeString("")
    assert render_styles({"abc": 123.45}) == SafeString("abc:123.45;")
    assert render_styles({"padding": 0, "margin": "0 10", "line-height": Decimal('2.3')}) == SafeString(
        "padding:0;margin:0 10;line-height:2.3;"
    )

    assert (
        render(div({"style": render_styles({"min-width": "25px"})}, "cool"))
        == '<div style="min-width:25px;">cool</div>'
    )




def test_render_styles_escapes() -> None:
    assert render_styles({'"><': '><>"'}) == SafeString(
        safe_str="&quot;&gt;&lt;:&gt;&lt;&gt;&quot;;"
    )

def test_attrs_not_required() -> None:
    assert (
        render(div(p({"class": "ok"}, "neat", br, "ok"))) ==
        '<div><p class="ok">neat<br/>ok</p></div>'
    )

def test_works_for_int() -> None:
    assert render(5) == "5"
    assert render(div({}, -500)) == "<div>-500</div>"

def test_works_for_float() -> None:
    assert render(5.0) == "5.0"
    assert render(div({}, -123.456)) == "<div>-123.456</div>"

def test_works_for_decimal() -> None:
    assert render(Decimal("5.0")) == "5.0"
    assert render(div({}, Decimal("-123.456"))) == "<div>-123.456</div>"

def test_tag_repr() -> None:
    assert repr(img) == "Tag(name='img', self_closing=True)"

def test_render_number_attributes() -> None:
    assert render(div({"x": 1, "y": 2.01, "z": Decimal("3.02")})) == '<div x="1" y="2.01" z="3.02"></div>'

def test_templatize() -> None:
    def greet(name: str, age: int) -> Node:
        return html(
            head(title("hi, ", name)),
            body(
                div({"class": "content",
                     "blabla": "bla"},
                    # raw str / int
                    h1("hi ", name, "I'm ", age),
                    # tag
                    br,
                    # list
                    ["wow"],
                    # generator
                    (name for _ in range(3)))
            )
        )


    expected = """<html><head><title>hi, John Doe</title></head><body><div class="content" blabla="bla"><h1>hi John DoeI&#x27;m 100</h1><br/>wowJohn DoeJohn DoeJohn Doe</div></body></html>"""
    assert render(greet("John Doe", 100)) == expected

    templatized = templatize(greet)
    assert render(templatized(name="John Doe", age=100)) == expected

