from simple_html.attributes import (class_, enctype, href, method, placeholder,
                                    type_, value)
from simple_html.nodes import (a, br, button, div, form, input_, label, p,
                               SafeString, span)
from simple_html.render import render_node


def test_renders_no_children():
    node = a(attrs=[], nodes=[])

    assert render_node(node) == "<a/>"


def test_renders_children():
    node = p(attrs=[class_('pclass')],
             nodes=[
                 "hey!",
                 a(attrs=[href("http://google.com"),
                          class_('aclass')],
                   nodes=['link text',
                          span(nodes=["whatever"])]),
                 br()]
             )

    assert (
        render_node(node) == ('<p class="pclass">hey!<a href="http://google.com" '
                              'class="aclass">link text<span>whatever</span></a>'
                              '<br/></p>')
    )


def test_escapes_normal_strings():
    node = "some < string"

    assert render_node(node) == "some &lt; string"


def test_safe_strings_are_not_escaped():
    assert render_node(SafeString("some < string")) == "some < string"


def test_simple_form():
    node = form(
        [method('POST'), enctype('multipart/form-data')],
        [label([],
               ["Name",
                input_([type_('text'),
                        value('some_value'),
                        placeholder('example text')])
                ]),
         div([class_('button-container')],
             [button([],
                     ["Submit"])
              ])]
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
