import unittest
import util


class TestJoinUrlPath(unittest.TestCase):
    def test_empty_path(self):
        result = util.join_url_path([])
        self.assertEqual(result, '')

    def test_single_element_path(self):
        result = util.join_url_path(['path'])
        self.assertEqual(result, 'path')

    def test_multiple_elements_path(self):
        result = util.join_url_path(['path', 'to', 'resource'])
        self.assertEqual(result, 'path/to/resource')

    def test_path_with_slashes(self):
        result = util.join_url_path(['/path/', 'to/', '/resource/'])
        self.assertEqual(result, 'path/to/resource')

    def test_mixed_data_types(self):
        result = util.join_url_path(['path', 123, '/resource/', True])
        self.assertEqual(result, 'path/123/resource/True')

    def test_blank_elements(self):
        result = util.join_url_path(['', 'path', '', '/resource/', ''])
        self.assertEqual(result, 'path/resource')

    def test_non_string_elements(self):
        result = util.join_url_path([None, 123, True])
        self.assertEqual(result, 'None/123/True')


if __name__ == '__main__':
    unittest.main()
