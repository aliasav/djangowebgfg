# -*- coding: utf-8 -*-
'''
Content related models: Item, Measure, Source
'''
import datetime
import uuid
import logging
from django.db import models, IntegrityError
from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def process_datetime_to_string(this_date):
    '''
        Converts a datetime obj to a string:
        4 hours
    '''
    string = ''
    if not isinstance(this_date, datetime.datetime):
        return string

    current = datetime.datetime.now()
    diff = current - this_date.replace(tzinfo=None)
    hours = int(diff.seconds / 3600)
    days = diff.days
    string = ''
    if ((days == 0) and (hours == 0 or hours == 1)):
        string = 'Just now'
    elif ((days == 0) and (hours > 1 and hours <= 24)):
        string = str(hours) + ' hours ago'
    elif days == 1:
        string = 'Yesterday'
    elif (days > 1 and days < 7):
        string = str(days) + ' days ago'
    elif days >= 7:
        string = str(this_date.strftime('%d %b %Y'))
    elif diff.days < 0:
        string = 'Just now'

    return string


class VocabItem(models.Model):
    '''Vocabulary Item model
    '''
    # word (eng): unique and indexed
    word = models.CharField(max_length=512, unique=True, db_index=True)

    # origin (eng)
    origin = models.TextField(null=True, blank=True)

    # single meaning
    meaning = models.TextField(null=True, blank=True)

    # if multiple meaning exist for the word
    meanings = ArrayField(models.TextField(null=True, blank=True),
                          default=list, null=True, blank=True)

    # part of speech
    pos = models.CharField(max_length=300, null=True, blank=True)

    # sentences with the word in it
    sentences = ArrayField(models.TextField(null=True, blank=True), default=list,
                           null=True, blank=True)

    # any other misc information about the word
    misc = JSONField(default=dict, null=True, blank=True)

    synonyms = ArrayField(models.CharField(max_length=100, null=True, blank=True),
                          default=list, null=True, blank=True)

    antonyms = ArrayField(models.CharField(max_length=100, null=True, blank=True),
                          default=list, null=True, blank=True)

    pronunciation = models.CharField(max_length=200, null=True, blank=True)

    audio_file_link = models.URLField(max_length=300, null=True, blank=True)

    # if True, this vocab item will be updated by a cron
    mark_for_update = models.BooleanField(default=False)

    # flag to mark if this vocab item should be used
    is_live = models.BooleanField(default=True)

    # timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'VocabItem: {0}<-->{1}'.format(self.word, self.id)

    def get_absolute_url(self):
        absolute_url = '/dictionary/' + str(self.word)
        return absolute_url

    def get_json(self):
        '''returns a serialized object
        '''
        data = {
            'id': self.id,
            'word': self.word,
            'origin': self.origin,
            'meaning': self.meaning,
            'meanings': self.meanings,
            'sentences': self.sentences,
            'pos': self.pos,
            'pronunciation': self.pronunciation,
            'audio_file_link': self.audio_file_link,
            'synonyms': self.synonyms[:5] if isinstance(self.synonyms, list) else [],
            'antonyms': self.antonyms[:5] if isinstance(self.antonyms, list) else [],
            'is_live': self.is_live,
        }

        sentences = []
        # check if sentences is NoneType
        if isinstance(self.sentences, list) and len(self.sentences) > 2:
            sentences = self.sentences[0:2]
        data['sentences'] = sentences

        return data

