from simple_html.attributes import (
    class_,
    enctype,
    href,
    method,
    placeholder,
    src,
    type_,
    value,
)
from simple_html.nodes import (
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
    SafeString,
    script,
    span,
)
from simple_html.render import render

import json


def test_renders_no_children() -> None:
    node = a()

    assert render(node) == "<a></a>"


def test_renders_children() -> None:
    node = p.attrs(class_("pclass"))(
        "hey!",
        a.attrs(href("https://google.com"),
                class_("aclass"))(
            "link text",
            span("whatever")
        ),
        br,
    )

    assert render(node) == (
        '<p class="pclass">hey!<a href="https://google.com" '
        'class="aclass">link text<span>whatever</span></a>'
        "<br/></p>"
    )


def test_hello_world() -> None:
    node = html(
        head,
        body(
            p.attrs(("class", "some-class"))(
                "Hello World!"
            )
        )
    )

    assert render(node) == (
        '<html><head></head><body><p class="some-class">Hello World!</p>'
        "</body></html>"
    )


def test_string_attrs_work_as_expected() -> None:
    node = div.attrs(("class", "dinosaur"),
                     ("some-random-attr", "spam"))
    assert render(node) == '<div class="dinosaur" some-random-attr="spam"></div>'


def test_escapes_normal_strings() -> None:
    node = "some < string"

    assert render(node) == "some &lt; string"


def test_safe_strings_are_not_escaped() -> None:
    assert render(SafeString("some < string")) == "some < string"


def test_simple_form() -> None:
    node = form.attrs(method("POST"),
                      enctype("multipart/form-data"))(
        label(
            "Name",
            input_.attrs(type_("text"),
                         value("some_value"),
                         placeholder("example text"))
        ),
        div.attrs(class_("button-container"))(
            button("Submit")
        ),
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
    node = script.attrs(type_("ld+json"))(
        SafeString(
            json.dumps({"some_key": "some_val"})
        )
    )

    assert render(node) == (
        '<script type="ld+json">{"some_key": "some_val"}</script>'
    )


def test_script_tag_doesnt_self_close() -> None:
    example_script_url = "https://example.com/main.js"

    node = script.attrs(src(example_script_url))
    assert render(node) == f'<script src="{example_script_url}"></script>'


def test_kw_attributes() -> None:
    node = div.attrs(class_("first"),
                     name="some_name",
                     style="color:blue;")("okok")

    assert render(node) == \
           '<div class="first" name="some_name" style="color:blue;">okok</div>'


def test_uncalled_tag_renders() -> None:
    assert render(a) == "<a></a>"
    assert render(br) == "<br/>"
