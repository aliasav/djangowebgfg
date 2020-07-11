# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.views import APIView

from content.models import VocabItem

logger = logging.getLogger(__name__)

@api_view(['GET'])
def vocab_item_detail(request, word):
    '''Returns detail of a vocab item
    '''
    # word falsy value check
    if not word:
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Word is invalid')

    vocab_item_qset = VocabItem.objects.filter(word=word)
    # check in db
    if not vocab_item_qset:
        return Response(status=status.HTTP_404_NOT_FOUND, data='Word not found!')
    
    # fetch vocab item
    vocab_item = vocab_item_qset[0]

    # serialize object
    data = vocab_item.get_json()

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
def vocab_item_update(request):
    '''Updates a vocab item
        POST API:
            data: word, meaning, meanings, misc, synonyms, antonyms ...
            (keys same as VocabItem model)
            - parse the data within the POST API
            - fetch the word
            - if the word exists, update fields and return success
    '''
    data = request.data
    word = data.get('word')
    
    # check word for falsy value
    if not word:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # fetch word from the db
    
    # update the word
    return Response(status=status.HTTP_200_OK)


class VocabItemListAPI(APIView):
    '''Vocab Item listing API
    '''
    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class VocabItemDetailAPI(APIView):
    '''Vocab Item Detail API
    '''
    def get(self, request, word):
        logger.debug(f'GET APIView class for {word}')

        # word falsy value check
        if not word:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Word is invalid')

        vocab_item_qset = VocabItem.objects.filter(word=word)
        # check in db
        if not vocab_item_qset:
            return Response(status=status.HTTP_404_NOT_FOUND, data='Word not found!')
        
        # fetch vocab item
        vocab_item = vocab_item_qset[0]

        # serialize object
        data = vocab_item.get_json()

        return Response(data=data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        word = data.get('word')

        logger.debug(f'POST API View: {request.data}')
        
        # check word for falsy value
        if not word:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # fetch word from the db
        
        # update the word
        
        return Response(status=status.HTTP_200_OK)
