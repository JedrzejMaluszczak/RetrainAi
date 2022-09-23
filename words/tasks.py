import requests
from celery.utils.log import get_task_logger
from django.db import transaction

from config.celery import app
from words.services.data_storage.word_dao import WordDAO

logger = get_task_logger(__name__)


@app.task()
def count_words_occurrences_in_file(file_path: str):
    """
    Celery task which counts words occurrences in file

    Parameters
    ----------
    file_path: str
        path to file in local system
    """
    logger.info("counting words in file...")
    with transaction.atomic(), open(file_path, "r") as file:
        for line in file:
            for word in line.split():
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
