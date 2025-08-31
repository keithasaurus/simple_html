from decimal import Decimal
from typing import Union, Generator, Any, Literal

import pytest

from simple_html import Node, SafeString, Tag, h1
from simple_html.templatize import _is_valid_node_annotation, Templatizable, find_invalid_annotations

test_annotations = [
    # Basic valid Node types
    (Node, True, "Direct Node type"),
    (str, True, "Basic string type"),
    (int, True, "Basic int type"),
    (float, True, "Basic float type"),
    (Decimal, True, "Decimal type"),
    (SafeString, True, "SafeString type"),
    (Tag, True, "Tag type"),

    # Basic invalid types
    (bool, False, "bool is not a valid Node type"),
    (type(None), False, "None type"),
    (dict, False, "dict type"),
    (set, False, "set type"),
    (bytes, False, "bytes type"),
    (complex, False, "complex number type"),
    (Exception, False, "Exception type"),

    # List types - valid
    (list[Node], True, "List of Nodes"),
    (list[str], True, "List of strings"),
    (list[int], True, "List of ints"),
    (list[float], True, "List of floats"),
    (list[Decimal], True, "List of Decimals"),
    (list[SafeString], True, "List of SafeStrings"),
    (list[Tag], True, "List of Tags"),

    # List types - invalid
    (list[bool], False, "List of bools"),
    (list[dict[str, str]], False, "List of dicts"),
    (list[set[str]], False, "List of sets"),
    (list[bytes], False, "List of bytes"),

    # Union types - all valid
    (Union[Node, str], True, "Union with Node and str"),
    (Union[str, int], True, "Union of valid types"),
    (Union[Node, int, float], True, "Union with multiple valid types"),
    (Union[SafeString, Tag], True, "Union of SafeString and Tag"),
    (Union[list[Node], str], True, "Union of list[Node] and str"),

    # Union types - with invalid members
    (Union[bool, str], False, "Union with invalid bool"),
    (Union[Node, dict], False, "Union with invalid dict"),
    (Union[str, int, bool], False, "Union mixing valid and invalid"),
    (Union[list[bool], str], False, "Union with invalid list[bool]"),

    # Optional types (Union with None)
    (Union[Node, None], True, "Optional Node"),
    (Union[str, None], True, "Optional str"),
    (Union[list[Node], None], True, "Optional list[Node]"),
    (Union[bool, None], False, "Optional bool (still invalid)"),

    # Tuple types - TagTuple structures (valid)
    (tuple[str, tuple[Node, ...], str], True, "TagTuple structure"),
    (tuple[str, tuple[str, ...], str], True, "TagTuple with strings"),
    (tuple[str, tuple[int, ...], str], True, "TagTuple with ints"),
    (tuple[str, tuple[SafeString, ...], str], True, "TagTuple with SafeStrings"),
    (tuple[str, tuple[Union[Node, str], ...], str], True, "TagTuple with Union types"),

    # Tuple types - invalid structures
    (tuple[int, str], False, "Invalid tuple structure (wrong length)"),
    (tuple[str, str, str], False, "Invalid tuple structure (middle not tuple)"),
    (tuple[int, tuple[Node, ...], str], False, "Invalid tuple structure (first not str)"),
    (tuple[str, tuple[Node, ...], int], False, "Invalid tuple structure (last not str)"),
    (tuple[str, tuple[bool, ...], str], False, "TagTuple with invalid bool"),
    (tuple[str, list[Node], str], False, "TagTuple with list instead of tuple"),

    # Generator types
    (Generator[Node, None, None], True, "Generator of Nodes"),
    (Generator[str, None, None], True, "Generator of strings"),
    (Generator[int, None, None], True, "Generator of ints"),
    (Generator[SafeString, None, None], True, "Generator of SafeStrings"),
    (Generator[bool, None, None], False, "Generator of bools"),
    (Generator[dict[str, str], None, None], False, "Generator of dicts"),
    (Generator[Union[Node, str], None, None], True, "Generator of Union types"),
    (Generator[list[Node], None, None], True, "Generator of list[Node]"),

    # Complex nested structures
    (list[tuple[str, tuple[Node, ...], str] | str | SafeString], True, "Complex nested Union"),
    (list[Union[Node, str, int]], True, "List of Union with valid types"),
    (list[Union[bool, str]], False, "List of Union with invalid bool"),
    (Union[list[Node], tuple[str, tuple[Node, ...], str]], True, "Union of complex types"),
    (list[list[Node]], True, "Nested list of Nodes"),
    (list[list[str]], True, "Nested list of strings"),
    (list[list[bool]], False, "Nested list of bools"),

    # Generator with complex types
    (Generator[tuple[str, tuple[Node, ...], str], None, None], True, "Generator of TagTuples"),
    (Generator[Union[Node, str], None, None], True, "Generator of Union types"),
    (Generator[list[Node], None, None], True, "Generator of list[Node]"),

    # Edge cases with deeply nested types
    (list[Union[tuple[str, tuple[Node, ...], str], Node, str]], True, "Deeply nested valid types"),
    (Union[Generator[Node, None, None], list[str]], True, "Union of Generator and list"),
    (list[Generator[Node, None, None]], True, "List of Generators"),
    (tuple[str, tuple[Union[Node, SafeString, str], ...], str], True, "TagTuple with complex Union"),

    # More invalid edge cases
    (tuple[str, tuple[Union[bool, str], ...], str], False, "TagTuple with invalid Union"),
    (list[tuple[str, str, str]], False, "List of invalid tuples"),
    (Union[Generator[bool, None, None], str], False, "Union with invalid Generator"),
    (list[Union[dict[int, int], str]], False, "List with invalid Union member"),

    # Types that might be confused with valid ones
    (type, False, "type itself"),
    (object, False, "object type"),
    (any, False, "any (lowercase)") if 'any' in globals() else (str, True, "any not defined"),

    # Additional container types that should be invalid
    (tuple[Node], False, "Single-element tuple (not TagTuple)"),
    (tuple[Node, str], False, "Two-element tuple (not TagTuple)"),
    (tuple[str, tuple[Node, ...], str, int], False, "Four-element tuple"),
]


@pytest.mark.parametrize('annotation,expected_result,description', test_annotations)
def test_annotation(annotation: Any, expected_result: bool, description: str) -> None:
    assert _is_valid_node_annotation(annotation) is expected_result, description


# Note: The actual test functions need to be defined properly for this to work
def process_node(node: Node, a: None) -> Node:
    return node


def process_node_1() -> Node:
    return h1


def process_node_2(a: list[str], b: str, c: list[Node]) -> Node:
    return h1


def process_node_3(a: bool) -> Node:
    return h1


def process_node_4(x: tuple[str, tuple[Node, ...], str]) -> Node:
    return h1


def process_node_5(x: list[tuple[str, tuple[Node, ...], str] | str | SafeString]) -> Node:
    return h1

def process_node_6(a, b) -> Node:  # type: ignore[no-untyped-def]
    return h1


# Test the validation
test_functions: list[tuple[Templatizable, Union[list[tuple[str, Any]], Literal["no_args"], None], str]] = [
    (process_node, [("a", None)], "None annotation should fail"),
    (process_node_1, "no_args", "should warn that there are no parameters"),
    (process_node_2, None, "mixed valid types should pass"),
    (process_node_3, [("a", bool)], "bool should fail"),
    (process_node_4, None, "TagTuple should pass"),
    (process_node_5, None, "complex nested Union should pass"),
    (process_node_6, None, "unannotated args should pass"),
]
@pytest.mark.parametrize('func,expected_result,description', test_functions)
def test_annotations_are_properly_checked_on_functions(func: Templatizable, expected_result: Union[list[tuple[str, Any]], Literal["no_args"], None], description: str) -> None:
    assert find_invalid_annotations(func) == expected_result, description
