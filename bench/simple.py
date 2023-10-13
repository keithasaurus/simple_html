from typing import List, Tuple

from simple_html.nodes import h1, html, title, head, body, div, p, ul, li, SafeString, br
from simple_html.render import render, render_with_doctype


def hello_world_empty(objs: list[None]) -> None:
    for _ in objs:
        render(h1("Hello, World!"))


def basic(objs: List[Tuple[str, str, List[str]]]) -> None:
    for title_, content, oks in objs:
        render_with_doctype(
            html(
                head(title(title_)),
                body(
                    h1.attrs({"class": "great header",
                              "other_attr": "5",
                              "id": "header1"}),
                    div(
                        p(content,
                          br,
                          br),
                        ul(
                            *[
                                li.attrs({"class": "item-stuff"})(SafeString(ss))
                                for ss in oks
                            ]
                        ),
                    ),
                    h1.attrs({"class": "great header",
                              "other_attr": "5",
                              "id": "header1"}),
                    div(
                        p(content,
                          br,
                          br),
                        ul(
                            *[
                                li.attrs({"class": "item-stuff"})(SafeString(ss))
                                for ss in oks
                            ]
                        ),
                    ),
                    h1.attrs({"class": "great header",
                              "other_attr": "5",
                              "id": "header1"}),
                    div(
                        p(content,
                          br,
                          br),
                        ul(
                            *[
                                li.attrs({"class": "item-stuff"})(SafeString(ss))
                                for ss in oks
                            ]
                        ),
                    ),
                    h1.attrs({"class": "great header",
                              "other_attr": "5",
                              "id": "header1"}),
                    div(
                        p(content,
                          br,
                          br),
                        ul(
                            *[
                                li.attrs({"class": "item-stuff"})(SafeString(ss))
                                for ss in oks
                            ]
                        ),
                    ),
                    h1.attrs({"class": "great header",
                              "other_attr": "5",
                              "id": "header1"}),
                    div(
                        p(content,
                          br,
                          br),
                        ul(
                            *[
                                li.attrs({"class": "item-stuff"})(SafeString(ss))
                                for ss in oks
                            ]
                        ),
                    ),
                ),
            )
        )
