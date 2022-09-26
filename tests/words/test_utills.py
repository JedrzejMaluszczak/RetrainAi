from django.test import TestCase

from words.utills import create_regex_from_string


class TestCreateRegexFunction(TestCase):
    def test_create_regex_without_special_characters(self):
        delimiters = [",", "k", '1']
        expected_output = "[,k1\\n]"
        # include newline
        regex = create_regex_from_string(delimiters=delimiters)

        self.assertEqual(expected_output, regex)

        # exclude newline
        expected_output = "[,k1]"
        regex = create_regex_from_string(delimiters=delimiters, include_newline=False)

        self.assertEqual(expected_output, regex)

    def test_create_regex_wit_special_characters(self):
        delimiters = [",", "k", '1', "$", "(", "="]
        expected_output = r"[,k1/\$//\(/=\n]"
        # include newline
        regex = create_regex_from_string(delimiters=delimiters)

        self.assertEqual(expected_output, regex)

        # exclude newline
        expected_output = "[,k1/\\$//\\(/=]"
        regex = create_regex_from_string(delimiters=delimiters, include_newline=False)

        self.assertEqual(expected_output, regex)
