# list of special regex character that must be escaped
from typing import List

REGEX_SPECIAL_CHARACTERS = r".^$*+-?()[]{}\|—/"


def read_chunks(file_obj, chunk_size=1000):
    """
    Generator
    Reads file in chunks

    Parameters
    ----------
    file_obj:
        File to read
    chunk_size:
        Size of chunks
    """
    while True:
        data = file_obj.read(chunk_size)
        if not data:
            break
        yield data


def create_regex_from_string(delimiters: List[str], include_newline=True):
    """
    Create regex containing given chars
    Parameters
    ----------
    delimiters: List(str)
        list of characters which should be included in regex pattern
    include_newline: bool
        flag telling if newline should be included in regex pattern
    Returns
    -------
    string
        regex pattern combined from given input
    """
    regex = ""
    for char in delimiters:
        if char in REGEX_SPECIAL_CHARACTERS:
            regex += f"/\{char}/"
        else:
            regex += char
    if include_newline:
        regex += r"\n"
    return f"[{regex}]"
