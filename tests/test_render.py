import json

from simple_html.nodes import (
    FlatGroup,
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
)
from simple_html.render import render, render_with_doctype


def test_renders_no_children() -> None:
    node = a()

    assert render(node) == "<a></a>"


def test_renders_children() -> None:
    node = p.attrs({"class": "pclass"})(
        "hey!",
        a.attrs({"href": "https://google.com", "class": "aclass"})(
            "link text", span("whatever")
        ),
        br,
    )

    assert render(node) == (
        '<p class="pclass">hey!<a href="https://google.com" '
        'class="aclass">link text<span>whatever</span></a>'
        "<br/></p>"
    )


def test_hello_world() -> None:
    node = html(head, body(p.attrs({"class": "some-class"})("Hello, World!")))

    assert render(node) == (
        '<html><head></head><body><p class="some-class">Hello, World!</p>'
        "</body></html>"
    )


def test_string_attrs_work_as_expected() -> None:
    node = div.attrs({"class": "dinosaur",
                      "some-random-attr": "spam"})
    assert render(node) == '<div class="dinosaur" some-random-attr="spam"></div>'


def test_escapes_normal_strings() -> None:
    node = "some < string"

    assert render(node) == "some &lt; string"


def test_safe_strings_are_not_escaped() -> None:
    assert render(SafeString("some < string")) == "some < string"


def test_simple_form() -> None:
    node = form.attrs({"method": "POST", "enctype": "multipart/form-data"})(
        label(
            "Name",
            input_.attrs({
                "type": "text",
                "value": "some_value",
                "placeholder": "example text"
            }),
        ),
        div.attrs({"class": "button-container"})(button("Submit")),
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
    node = script.attrs({"type": "ld+json"})(
        SafeString(json.dumps({"some_key": "some_val"}))
    )

    assert render(node) == ('<script type="ld+json">{"some_key": "some_val"}</script>')


def test_script_tag_doesnt_self_close() -> None:
    example_script_url = "https://example.com/main.js"

    node = script.attrs({"src": example_script_url})
    assert render(node) == f'<script src="{example_script_url}"></script>'


def test_kw_attributes() -> None:
    node = div.attrs({"class": "first",
                      "name": "some_name",
                      "style": "color:blue;"})("okok")

    assert (
            render(node)
            == '<div class="first" name="some_name" style="color:blue;">okok</div>'
    )


def test_uncalled_tag_renders() -> None:
    assert render(a) == "<a></a>"
    assert render(br) == "<br/>"


def test_attribute_without_value_rendered_as_expected() -> None:
    assert render(a.attrs({"something": None})) == "<a something></a>"


def test_render_with_doctype() -> None:
    assert render_with_doctype(html) == "<!doctype html><html></html>"
    assert (
            render_with_doctype(html, "other info") == "<!doctype other info><html></html>"
    )


def test_render_flat_group() -> None:
    assert render(FlatGroup(br, "ok", div("great"))) == "<br/>ok<div>great</div>"

    assert render(FlatGroup()) == ""


def test_render_kw_attribute_with_none() -> None:
    assert render(script.attrs({"defer": None})) == "<script defer></script>"


def test_can_render_none() -> None:
    assert render(None) == ""
    assert (
            render(div(None, "hello ", None, span("World!"), None))
            == "<div>hello <span>World!</span></div>"
    )
