from django.db import models


class WordOccurrence(models.Model):
    """
    A class used to represent word occurrences

    Attributes
    ----------
    word: models.TextField
        represent a word value of unlimited length (depends on db)
    number_of_occurrence: PositiveIntegerField
        number of occurrence of given word in text
    """

    word = models.TextField(blank=False, null=False, unique=True)
    number_of_occurrence = models.PositiveIntegerField(default=1)
