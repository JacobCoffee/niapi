"""Test app/utils.py."""

import re
import string
from dataclasses import dataclass

import hypothesis.strategies as st
from hypothesis import given

from app.utils import camel_case, case_insensitive_string_compare, check_email, dataclass_as_dict_shallow, slugify


@given(st.emails())
def test_check_email(email: str) -> None:
    assert check_email(email) == email.lower()


@given(st.text(alphabet=string.ascii_letters + string.digits + string.whitespace + "-"))
def test_slugify(value: str) -> None:
    if all(c in string.whitespace or c == "-" for c in value):
        assert slugify(value) == re.sub(r"[-\s]+", "-", value.lower()).strip("-_")
    else:
        assert slugify(value)


@given(st.text(st.characters(blacklist_characters="_")))
def test_camel_case(string: str) -> None:
    assert camel_case(string) == "".join(
        word if index == 0 else word.capitalize() for index, word in enumerate(string.split("_"))
    )


@given(st.text(), st.text())
def test_case_insensitive_string_compare(a: str, b: str) -> None:
    assert case_insensitive_string_compare(a, b) == (a.strip().lower() == b.strip().lower())


@given(st.text(min_size=1), st.integers())
def test_dataclass_as_dict_shallow(name: str, value: int) -> None:
    @dataclass
    class TestClass:
        var: int = 1

    test_class = TestClass(value)
    assert dataclass_as_dict_shallow(test_class) == {"var": value}


def test_module_to_os_path() -> None:
    pass


def test_import_string() -> None:
    pass
