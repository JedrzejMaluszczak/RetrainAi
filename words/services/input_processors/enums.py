from enum import Enum


class InputTypeEnum(Enum):
    """
    Enum used to store valid input_type options
    """

    FILE_PATH = ("file_path",)
    STRING = ("string",)
    URL = "url"
