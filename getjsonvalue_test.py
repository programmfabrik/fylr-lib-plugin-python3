import pytest
from . import util


def test_valid_path():
    data = {'a': {'b': {'c': 42}}}
    assert util.get_json_value(data, 'a.b.c') == 42


def test_invalid_path_with_default():
    data = {'a': {'b': {'c': 42}}}
    assert util.get_json_value(data, 'a.b.d', default=99) == 99


def test_invalid_path_with_expected():
    data = {'a': {'b': {'c': 42}}}
    with pytest.raises(Exception) as exc_info:
        util.get_json_value(data, 'a.b.d', expected=True)
    assert str(exc_info.value) == 'expected: d'


def test_nested_path_with_escape_character():
    data = {'a': {'b.c': 42}}
    assert util.get_json_value(data, 'a.b\\.c') == 42


def test_non_dict_values():
    data = {'a': {'b': 10}}
    assert util.get_json_value(data, 'a.b.c', default=99) == 99


def test_empty_path():
    data = {'a': {'b': {'c': 42}}}
    assert util.get_json_value(data, '') == data


def test_custom_split_char():
    data = {'a': {'b': {'c': 42}}}
    assert util.get_json_value(data, 'a/b/c', split_char='/') == 42
