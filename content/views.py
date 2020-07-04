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
    template = 'base.html'
    context = {'word': 'example'}
    return render(request, template, context)


def word_view(request, word=None):
    template = 'word.html'
    word_qset = VocabItem.objects.filter(word=word)
    context = {}
    if word_qset:
        word = word_qset[0]
        context = word.get_json()

    return render(request, template, context)


