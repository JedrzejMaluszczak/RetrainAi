import string

from django.db.models import F

from words.models import WordOccurrence


class WordDAO:
    """
    Data Access Object for WordOccurrence model
    """

    @staticmethod
    def persist_word(word: str):
        """
        Save given word into database as lowercase without punctuation marks.
        If word already exists in db, increment value of occurrences by 1

        Parameters
        ----------
        word: str
            word to save
        """
        word = word.translate(str.maketrans('', '', string.punctuation))
        obj, created = WordOccurrence.objects.get_or_create(word=word.lower().strip())
        if not created:
            obj.number_of_occurrence = F("number_of_occurrence") + 1
            obj.save()

    @staticmethod
    def get_word_occurrences(word: str):
        """
        Returns number of occurrences of given word
        Parameters
        ----------
        word: str
            word whose number of occurrences we want to get
        """
        obj = WordOccurrence.objects.filter(word=word.lower()).first()
        return obj.number_of_occurrence if obj else 0
