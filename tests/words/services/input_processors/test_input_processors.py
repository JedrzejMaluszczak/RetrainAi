from django.core.exceptions import ValidationError
from django.test import TestCase

from words.services.input_processors.input_processors import (
    AbstractWordCounterFileInputProcessor,
    AbstractWordCounterStringInputProcessor,
    AbstractWordCounterURLInputProcessor,
)


class TestWordCounterFileInputProcessor(TestCase):
    def test_validation_raise_exception(self):
        processor = AbstractWordCounterFileInputProcessor("somerandomfilepath.txt")
        self.assertRaises(ValidationError, processor.validate)

    def test_correct_filepath_validation(self):
        AbstractWordCounterFileInputProcessor("tests/test_files/test.txt")


class TestWordCounterStringInputProcessor(TestCase):
    def test_validation_raise_exception(self):
        processor = AbstractWordCounterStringInputProcessor("")
        self.assertRaises(ValidationError, processor.validate)

        processor = AbstractWordCounterStringInputProcessor(None)
        self.assertRaises(ValidationError, processor.validate)

    def test_correct_input_validation(self):
        processor = AbstractWordCounterStringInputProcessor("word word word")
        processor.validate()


class TestWordCounterURLInputProcessor(TestCase):
    def test_validation_raise_exception(self):
        processor = AbstractWordCounterURLInputProcessor("")
        self.assertRaises(ValidationError, processor.validate)

        processor = AbstractWordCounterURLInputProcessor("gooasdasda .asd a.asd as.d asd")
        self.assertRaises(ValidationError, processor.validate)

        processor = AbstractWordCounterURLInputProcessor("google.com")
        self.assertRaises(ValidationError, processor.validate)

    def test_correct_url_validation(self):
        processor = AbstractWordCounterURLInputProcessor("https://www.google.com/")
        processor.validate()

        processor = AbstractWordCounterURLInputProcessor("https://www.retrain.ai/company/careers/")
        processor.validate()
