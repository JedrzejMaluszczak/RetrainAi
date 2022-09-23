from words.services.input_processors.enums import InputTypeEnum
from words.services.input_processors.input_processors import (
    AbstractWordCounterInputProcessor,
    AbstractWordCounterFileInputProcessor,
    AbstractWordCounterStringInputProcessor,
    AbstractWordCounterURLInputProcessor,
)


def get_input_processor(value: str, input_type: str) -> AbstractWordCounterInputProcessor:
    """
    Create and return different type of Input Processor depends on input_type

    Parameters
    ----------
    value: str
        value used to initialize input processor
        should be filepath, url or string
    input_type: str
        used to identify input type
        should be a member of InputTypeEnum
    """
    k = InputTypeEnum[input_type.upper()]

    input_processor = {
        InputTypeEnum.FILE_PATH: AbstractWordCounterFileInputProcessor,
        InputTypeEnum.STRING: AbstractWordCounterStringInputProcessor,
        InputTypeEnum.URL: AbstractWordCounterURLInputProcessor,
    }[k]

    return input_processor(value)
