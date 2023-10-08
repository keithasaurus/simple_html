import time

from simple_html.attributes import class_
from simple_html.nodes import SafeString, body, div, h1, head, html, li, p, title, ul
from simple_html.render import render_with_doctype

time_start = time.time()

for i in range(20000):
    node = html(
        head(title("some title")),
        body(
            h1.attrs(class_("great header"), ("other_attr", "5"), id="header1"),
            div(
                p("some content"),
                ul(
                    *[
                        li.attrs(class_("item-stuff"))(SafeString("okokok"))
                        for _ in range(10)
                    ]
                ),
            ),
        ),
    )
    x = render_with_doctype(node)

print(time.time() - time_start, "seconds")
