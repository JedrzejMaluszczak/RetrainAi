from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from words.services.data_storage.word_dao import WordDAO
from words.services.input_processors.input_processors_dispatcher import get_input_processor


class WordApiView(ViewSet):
    @action(detail=False, methods=['post'])
    def word_counter(self, request):
        value = request.data.get('value')
        input_type = request.data.get('input_type')
        try:
            processor = get_input_processor(value=value, input_type=input_type)
            processor.validate()
            processor.process()
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Wrong input type!")
        except ValidationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e.message)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def word_statistics(self, request):
        word: str = request.GET.get("word", None)
        if not word:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Incorrect input!")

        number_of_occurrence = WordDAO.get_word_occurrences(word)
        return Response(status=status.HTTP_200_OK, data=number_of_occurrence)
