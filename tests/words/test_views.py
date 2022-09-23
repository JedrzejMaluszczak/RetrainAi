from django.test import TestCase
from django.test.client import Client
from rest_framework import status

from words.models import WordOccurrence


class TestWordApiView(TestCase):
    def setUp(self):
        self.test_word = "word"
        WordOccurrence.objects.create(word=self.test_word)
        self.client = Client()

    def test_word_counter_view(self):
        response = self.client.get("/word_statistics/", data={"word": "someWord"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 0)

        response = self.client.get("/word_statistics/", data={"word": self.test_word})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 1)

    def test_word_counter_view_faild(self):
        response = self.client.get("/word_statistics/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Incorrect input!")

    def test_word_counter(self):
        data = {
            "input_type": "string",
            "value": "value",
        }
        response = self.client.post("/word_counter/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_word_counter_wrong_input_type(self):
        data = {
            "input_type": "WrongInputType",
            "value": "value",
        }
        response = self.client.post("/word_counter/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Wrong input type!")

    def test_word_counter_string_validation_error(self):
        data = {
            "input_type": "string",
            "value": "",
        }
        response = self.client.post("/word_counter/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Incorrect data!")

    def test_word_counter_file_validation_error(self):
        file_path = "test/test/test/"
        data = {
            "input_type": "file_path",
            "value": file_path,
        }
        response = self.client.post("/word_counter/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, f"File with path:{file_path} does not exists!")

    def test_word_counter_url_validation_error(self):
        url = "test/test/test/"
        data = {
            "input_type": "url",
            "value": url,
        }
        response = self.client.post("/word_counter/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Enter a valid URL.")
