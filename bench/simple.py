from typing import List, Tuple

from simple_html.nodes import (
    h1,
    html,
    title,
    head,
    body,
    div,
    p,
    ul,
    li,
    safe_string,
    br, meta
)
from simple_html.render import render, render_with_doctype


def hello_world_empty(objs: List[None]) -> None:
    for _ in objs:
        render(h1("Hello, World!"))


def basic(objs: List[Tuple[str, str, List[str]]]) -> None:
    for title_, content, oks in objs:
        render_with_doctype(
            html(
                head(title(title_)),
                body(
                    h1.attrs(
                        {"class": "great header", "other_attr": "5", "id": "header1"}
                    ),
                    div(
                        p(content, br, br),
                        ul(
                            [
                                li.attrs({"class": "item-stuff"})(safe_string(ss))
                                for ss in oks
                            ]
                        ),
                    ),
                ),
            )
        )


def basic_long(objs: List[Tuple[str, str, List[str]]]) -> None:
    for title_, content, oks in objs:
        render_with_doctype(
            html(
                head(title(title_)),
                body(
                    h1.attrs(
                        {"class": "great header", "other_attr": "5", "id": "header1"}
                    ),
                    div(
                        p(content, br, br),
                        ul(
                            *[
                                li.attrs({"class": "item-stuff"})(safe_string(ss))
                                for ss in oks
                            ]
                        ),
                    ),
                    h1.attrs(
                        {"class": "great header", "other_attr": "5", "id": "header1"}
                    ),
                    div(
                        p(content, br, br),
                        ul(
                            *[
                                li.attrs({"class": "item-stuff"})(safe_string(ss))
                                for ss in oks
                            ]
                        ),
                    ),
                    h1.attrs(
                        {"class": "great header", "other_attr": "5", "id": "header1"}
                    ),
                    div(
                        p(content, br, br),
                        ul(
                            *[
                                li.attrs({"class": "item-stuff"})(safe_string(ss))
                                for ss in oks
                            ]
                        ),
                    ),
                    h1.attrs(
                        {"class": "great header", "other_attr": "5", "id": "header1"}
                    ),
                    div(
                        p(content, br, br),
                        ul(
                            *[
                                li.attrs({"class": "item-stuff"})(safe_string(ss))
                                for ss in oks
                            ]
                        ),
                    ),
                    h1.attrs(
                        {"class": "great header", "other_attr": "5", "id": "header1"}
                    ),
                    div(
                        p(content, br, br),
                        ul(
                            *[
                                li.attrs({"class": "item-stuff"})(safe_string(ss))
                                for ss in oks
                            ]
                        ),
                    ),
                ),
            )
        )


def lorem_ipsum(titles: str) -> None:
    for t in titles:
        render_with_doctype(
            html.attrs({"lang": "en"})(
                head(
                    meta.attrs({"charset": "UTF-8"}),
                    meta.attrs({"name": "viewport",
                                "content": "width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0"}),
                    meta.attrs({"http-equiv": "X-UA-Compatible",
                                "content": "ie=edge"}),
                    title(t)
                ),
                body(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                )
            )
        )
