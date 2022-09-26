import re

import requests
from celery.utils.log import get_task_logger
from django.db import transaction
from typing import List

from config.celery import app
from words.services.data_storage.word_dao import WordDAO
from words.utills import read_chunks, create_regex_from_string

logger = get_task_logger(__name__)


@app.task()
def count_words_occurrences_in_file(
        file_path: str,
        delimiters: List[str],
        split_on_new_line=True,
):
    """
    Celery task which counts words occurrences in file

    Parameters
    ----------
    file_path: str
        path to file in local system
    delimiters: str
        list of characters which separate words
    split_on_new_line: bool
        flag telling if string should be split on new line
    """
    logger.info("counting words in file...")
    with transaction.atomic(), open(file_path, "r") as file:
        for data in read_chunks(file):
            if data[-1] not in delimiters:
                for char in read_chunks(file, 1):
                    if char in delimiters:
                        break
                    else:
                        data += char

            regex = create_regex_from_string(delimiters, split_on_new_line)
            temp = re.split(regex, data)
            temp[:] = [x for x in temp if x]

            for word in temp:
                WordDAO.persist_word(word)
    return True


@app.task()
def count_words_occurrences_in_string(text: str):
    """
    Celery task which counts words occurrences in string

    Parameters
    ----------
    text: str
        string whose words occurrences will be counted
    """
    logger.info("counting words in string...")
    with transaction.atomic():
        words = text.split()
        for word in words:
            WordDAO.persist_word(word)
    return True


@app.task()
def count_words_occurrences_file_from_url(url: str):
    """
    Celery task which counts words occurrences in file downloaded from url

    Parameters
    ----------
    url: str
        url to file
    """
    logger.info("counting words in remote file...")

    with transaction.atomic(), requests.Session().get(url, stream=True) as response:
        for line in response.iter_lines(decode_unicode=True):
            for word in line.split():
                WordDAO.persist_word(word)
    return True
