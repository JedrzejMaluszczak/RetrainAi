from django.test import TestCase

from words.models import WordOccurrence
from words.services.data_storage.word_dao import WordDAO


class TestWordDAO(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_word = "word"
        WordOccurrence.objects.create(word=cls.test_word)
        for i in range(0, 9):
            WordOccurrence.objects.create(word=f"word{i}")

    def test_persist_word(self):
        test_word = "single"

        WordDAO.persist_word(test_word)
        persisted_word = WordOccurrence.objects.get(word=test_word)

        self.assertEqual(persisted_word.word, test_word)
        self.assertEqual(persisted_word.number_of_occurrence, 1)

    def test_persist_word_with_punctuation(self):
        punctuation = ["!", "`", "$", "(", ")", "{", "}", "."]
        test_word = "single"
        for char in punctuation:
            test_word_with_punctuation = test_word + char
            WordDAO.persist_word(test_word_with_punctuation)

        persisted_word = WordOccurrence.objects.get(word=test_word)

        self.assertEqual(persisted_word.word, test_word)
        self.assertEqual(persisted_word.number_of_occurrence, len(punctuation))

    def test_persist_word_twice(self):
        WordDAO.persist_word(self.test_word)

        persisted_word = WordOccurrence.objects.get(word=self.test_word)

        self.assertEqual(persisted_word.word, self.test_word)
        self.assertEqual(persisted_word.number_of_occurrence, 2)

    def test_get_word_occurrences(self):
        WordOccurrence.objects.filter(word=self.test_word).update(number_of_occurrence=10)
        word_occurrences = WordDAO.get_word_occurrences(self.test_word)
        self.assertEqual(word_occurrences, 10)
