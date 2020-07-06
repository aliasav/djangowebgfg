'''Contains all views for content app
'''
from __future__ import unicode_literals

from django.shortcuts import render
from content.models import VocabItem


def home_view(request):
    '''renders home page
    '''    
    template = 'home.html'
    context = {}
    return render(request, template, context)


def base_view(request):
    '''renders base.html
    '''
    template = 'base.html'
    context = {'word': 'example'}
    return render(request, template, context)


def word_view(request, word=None):
    ''' renders a dictionary page
    ::word: passed in the URL as a param
    '''
    template = 'word.html' # template to load

    # fetch the word query set
    word_qset = VocabItem.objects.filter(word=word)
    context = {}

    # check if word exists
    if word_qset:
        word = word_qset[0]
        context = {
            'data': word.get_json()
        }
    return render(request, template, context)

def search_view(request, word=None):
    ''' renders a dictionary page
    ::word: passed in the URL as a param
    '''
    template = 'search.html' # template to load
    context = {}
    return render(request, template, context)
