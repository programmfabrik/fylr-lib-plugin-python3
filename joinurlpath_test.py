from . import util


def test_empty_path():
    result = util.join_url_path([])
    assert result == ''


def test_single_element_path():
    result = util.join_url_path(['path'])
    assert result == 'path'


def test_multiple_elements_path():
    result = util.join_url_path(['path', 'to', 'resource'])
    assert result == 'path/to/resource'


def test_path_with_slashes():
    result = util.join_url_path(['/path/', 'to/', '/resource/'])
    assert result == 'path/to/resource'


def test_mixed_data_types():
    result = util.join_url_path(['path', 123, '/resource/', True])
    assert result == 'path/123/resource/True'


def test_blank_elements():
    result = util.join_url_path(['', 'path', '', '/resource/', ''])
    assert result == 'path/resource'


def test_non_string_elements():
    result = util.join_url_path([None, 123, True])
    assert result == 'None/123/True'
