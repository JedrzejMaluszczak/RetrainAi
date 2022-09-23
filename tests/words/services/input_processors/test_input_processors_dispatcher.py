from django.test import TestCase

from words.services.input_processors.input_processors import (
    AbstractWordCounterURLInputProcessor,
    AbstractWordCounterFileInputProcessor,
    AbstractWordCounterStringInputProcessor,
)
from words.services.input_processors.input_processors_dispatcher import get_input_processor


class TestInputProcessorDispatcher(TestCase):
    def test_get_url_input_processor(self):
        processor = get_input_processor("value", input_type="URL")
        self.assertTrue(isinstance(processor, AbstractWordCounterURLInputProcessor))

        processor = get_input_processor("value", input_type="url")
        self.assertTrue(isinstance(processor, AbstractWordCounterURLInputProcessor))

        processor = get_input_processor("value", input_type="UrL")
        self.assertTrue(isinstance(processor, AbstractWordCounterURLInputProcessor))

    def test_get_file_input_processor(self):
        processor = get_input_processor("value", input_type="file_path")
        self.assertTrue(isinstance(processor, AbstractWordCounterFileInputProcessor))

        processor = get_input_processor("value", input_type="fIle_patH")
        self.assertTrue(isinstance(processor, AbstractWordCounterFileInputProcessor))

        processor = get_input_processor("value", input_type="FILE_PATH")
        self.assertTrue(isinstance(processor, AbstractWordCounterFileInputProcessor))

    def test_get_string_input_processor(self):
        processor = get_input_processor("value", input_type="string")
        self.assertTrue(isinstance(processor, AbstractWordCounterStringInputProcessor))

        processor = get_input_processor("value", input_type="STRING")
        self.assertTrue(isinstance(processor, AbstractWordCounterStringInputProcessor))

        processor = get_input_processor("value", input_type="stRIng")
        self.assertTrue(isinstance(processor, AbstractWordCounterStringInputProcessor))

    def test_wrong_input_type(self):
        self.assertRaises(KeyError, lambda: get_input_processor("value", input_type="SomeRAndomText"))
