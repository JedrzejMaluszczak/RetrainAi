from django.contrib import admin

from words.models import WordOccurrence


class WordOccurrenceAdmin(admin.ModelAdmin):
    list_display = ['word', 'number_of_occurrence']


admin.site.register(WordOccurrence, WordOccurrenceAdmin)
