'''Contains all views for content app
'''
from __future__ import unicode_literals

from django.shortcuts import render

# render -> HTTPResponse

# import logging

def home_view(request):
    '''renders home page
    '''    
    template = 'home/home.html'
    context = {}
    return render(request, template, context)

def base_view(request):
    template = 'base.html'
    context = {'word': 'example'}
    return render(request, template, context)

from content.models import VocabItem
def word_view(request, word=None):

    template = 'word.html'
    context = {
        'word': word,
    }

    qset = VocabItem.objects.filter(word=word)
    if qset:
        viobj = qset[0]
        data = viobj.get_json()
    context['data'] = {
        'id': 2186, 
        'word': 'rancid', 
        'origin': 'Early 17th century from Latin rancidus ‘stinking’.', 
        'meaning': '(of foods containing fat or oil) smelling or tasting unpleasant as a result of being old and stale.', 
        'meanings': ['(of foods containing fat or oil) smelling or tasting unpleasant as a result of being old and stale.'], 
        'sentences': ['rancid meat', 'rancid meat'], 
        'pos': 'adjective', 
        'pronunciation': None, 'score': 0.00319163404754896, 
        'audio_file_link': None, 
        'synonyms': ['sour', 'stale', 'turned', 'rank', 'putrid'], 
        'antonyms': [], 
        'mnemonics': [], 
        'is_live': True
    }
    return render(request, template, context)


