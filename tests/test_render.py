from simple_html.attributes import (class_, enctype, href, method, placeholder,
                                    src, type_, value)
from simple_html.nodes import (a, body, br, button, div, form, head, html,
                               input_, label, p, SafeString, script, span)
from simple_html.render import render_node

import json


def test_renders_no_children():
    node = a([])

    assert render_node(node) == "<a></a>"


def test_renders_children():
    node = p(
        [class_('pclass')],
        "hey!",
        a(
            [href("http://google.com"), class_('aclass')],
            'link text',
            span(
                [],
                "whatever"
            )
        ),
        br([])
    )

    assert (
        render_node(node) == ('<p class="pclass">hey!<a href="http://google.com" '
                              'class="aclass">link text<span>whatever</span></a>'
                              '<br/></p>')
    )


def test_hello_world():
    node = html(
        [],
        head(
            []
        ),
        body(
            [],
            p(
                [("class", "some-class")],
                "Hello World!"
            )
        )
    )

    assert render_node(node) == (
        '<html><head></head><body><p class="some-class">Hello World!</p>'
        '</body></html>'
    )


def test_string_attrs_work_as_expected():
    node = div(
        [('class', 'dinosaur'),
         ('some-random-attr', 'spam')]
    )
    assert render_node(node) == (
        '<div class="dinosaur" some-random-attr="spam"></div>'
    )


def test_escapes_normal_strings():
    node = "some < string"

    assert render_node(node) == "some &lt; string"


def test_safe_strings_are_not_escaped():
    assert render_node(SafeString("some < string")) == "some < string"


def test_simple_form():
    node = form(
        [method('POST'), enctype('multipart/form-data')],
        label(
            [],
            "Name",
            input_(
                [type_('text'), value('some_value'), placeholder('example text')]
            )
        ),
        div(
            [class_('button-container')],
            button(
                [],
                "Submit"
            )
        )
    )

    assert render_node(node) == (
        '<form method="POST" enctype="multipart/form-data">'
        '<label>Name'
        '<input type="text" value="some_value" placeholder="example text"/>'
        '</label>'
        '<div class="button-container">'
        '<button>Submit</button>'
        '</div>'
        '</form>'
    )


def test_safestring_in_tag():
    node = script(
        [type_('ld+json')],
        SafeString(json.dumps({
            'some_key': 'some_val'
        }))
    )

    assert render_node(node) == (
        '<script type="ld+json">{"some_key": "some_val"}</script>'
    )


def test_script_tag_doesnt_self_close():
    example_script_url = "http://example.com/main.js"

    node = script([src(example_script_url)])
    assert render_node(node) == f'<script src="{example_script_url}"></script>'
