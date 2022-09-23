import os.path
from abc import ABC, abstractmethod

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from words.tasks import (
    count_words_occurrences_in_file,
    count_words_occurrences_in_string,
    count_words_occurrences_file_from_url,
)


class AbstractWordCounterInputProcessor(ABC):
    """
    Base class for InputsProcessors
    """

    def __init__(self, value: str):
        self.value = value

    @abstractmethod
    def process(self):
        """
        Process input value
        """
        raise NotImplementedError

    @abstractmethod
    def validate(self):
        """
        Validate input value
        """
        raise NotImplementedError


class AbstractWordCounterFileInputProcessor(AbstractWordCounterInputProcessor):
    """
    Input processor for file input
    """

    def process(self):
        count_words_occurrences_in_file.delay(self.value)

    def validate(self):
        if not os.path.exists(self.value):
            raise ValidationError(f"File with path:{self.value} does not exists!")


class AbstractWordCounterStringInputProcessor(AbstractWordCounterInputProcessor):
    """
    Input processor for string input
    """

    def process(self):
        count_words_occurrences_in_string.delay(self.value)

    def validate(self):
        if not self.value:
            raise ValidationError(f"Incorrect data!")


class AbstractWordCounterURLInputProcessor(AbstractWordCounterInputProcessor):
    """
    Input processor for url input
    """

    def process(self):
        count_words_occurrences_file_from_url.delay(self.value)

    def validate(self):
        val = URLValidator()
        val(self.value)
        if not self.value:
            raise ValidationError(f"Incorrect data!")
