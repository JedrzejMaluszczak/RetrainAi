import requests_mock
from django.test import TestCase

from words.models import WordOccurrence
from words.tasks import (
    count_words_occurrences_in_file,
    count_words_occurrences_in_string,
    count_words_occurrences_file_from_url,
)


class TestCountWordsOccurrencesTask(TestCase):
    words_occurrences_in_file_dict = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
    }

    def test_count_words_occurrences_in_file(self):
        count_words_occurrences_in_file("tests/test_files/test.txt")

        for k, v in self.words_occurrences_in_file_dict.items():
            number_of_occurrence = WordOccurrence.objects.get(word=k).number_of_occurrence
            self.assertEqual(number_of_occurrence, v)

    def test_count_words_occurrences_in_string(self):
        count_words_occurrences_in_string("Word1? {word2 word2! word3. word1")

        number_of_occurrence = WordOccurrence.objects.get(word="word1").number_of_occurrence
        self.assertEqual(number_of_occurrence, 2)

        number_of_occurrence = WordOccurrence.objects.get(word="word2").number_of_occurrence
        self.assertEqual(number_of_occurrence, 2)

        number_of_occurrence = WordOccurrence.objects.get(word="word3").number_of_occurrence
        self.assertEqual(number_of_occurrence, 1)

    def test_count_words_occurrences_in_file_from_url(self):
        test_url = 'http://test.com'
        with requests_mock.mock() as m:
            with open("tests/test_files/test.txt", "r") as f:
                m.get(test_url, body=f)
                count_words_occurrences_file_from_url(test_url)

                for k, v in self.words_occurrences_in_file_dict.items():
                    number_of_occurrence = WordOccurrence.objects.get(word=k).number_of_occurrence
                    self.assertEqual(number_of_occurrence, v)
