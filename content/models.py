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


def get_default_action_counts():
    """
    Returns dict of default action counts
    """
    default = {
        'click': 0,
        'like': 0,
        'save': 0,
        'share': 0,
        'page-load-link': 0,
    }
    return default


class VocabItem(models.Model):
    '''Vocabulary Items
    '''
    # guid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)

    # word (eng)
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

    # score: function of actions, time decay and editorial bias
    # score = models.FloatField(default=0, null=True, blank=True)

    # editorial bias: used to grant higher scores to items
    # editorial_bias = models.FloatField(default=0, null=True, blank=True)

    # counts of actions on this item
    # maintains a dict of counts of each item
    # ever action updates counts in this json field
    # action_counts = JSONField(default=get_default_action_counts, null=True, blank=True)

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


# class Blog(models.Model):
#     '''Blog posts
#     '''
#     # article title
#     title = models.TextField(null=True, blank=False)

#     # slug title filled by admins
#     slug_title = models.CharField(max_length=255, null=True, blank=False)

#     # auto generated slug field
#     slug = models.SlugField(max_length=255, null=True, blank=False,
#                             unique=True)

#     # description of the item
#     description = models.TextField(null=True, blank=True)

#     # actual content of the item
#     content = models.TextField(null=True, blank=False)

#     # read time of article in seconds
#     read_time_value = models.IntegerField(default=0, null=True, blank=True)

#     # author of the blog post
#     author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

#     # associated categories of the item
#     category = ArrayField(models.CharField(max_length=100, null=True, blank=True), default=list)

#     # many-to-many field with vocab items
#     vocab_items = models.ManyToManyField('VocabItem', null=True, blank=True)

#     # flag to mark if this vocab item should be used
#     is_live = models.BooleanField(default=True)

#     # score: function of actions, time decay and editorial bias
#     score = models.FloatField(default=0, null=True, blank=True)

#     # editorial bias: used to grant higher scores to items
#     editorial_bias = models.FloatField(default=0, null=True, blank=True)

#     # mark for vocab item extraction
#     mark_for_update = models.BooleanField(default=True)

#     # language choices
#     INTERNAL_BLOG = 1
#     INTERVIEW_EXP = 2
#     PROMO_BLOG = 3
#     BLOG_TYPES = (
#         (INTERNAL_BLOG, 'Internal blog'),
#         (INTERVIEW_EXP, 'Interview experience blog'),
#         (PROMO_BLOG, 'Promotional blog'),
#     )
#     # type of blog
#     blog_type = models.IntegerField(default=INTERNAL_BLOG,
#                                     choices=BLOG_TYPES, null=True, blank=True)

#     # timestamp fields
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return 'Blog: {0}<-->{1}'.format(self.id, self.slug_title)

#     def get_absolute_url(self):
#         absolute_url = '/blog/' + str(self.id)
#         if self.slug:
#             absolute_url = '/blog/' + self.slug
#         return absolute_url

#     def get_json(self, user=None):
#         '''
#         return json dict of item
#         adds action flags if user is present
#         '''
#         data = {
#             'id': self.id,
#             'slug': self.slug,
#             'slug_title': self.slug_title,
#             'title': self.title,
#             'content': self.content,
#             'description':self.description,
#             'score': self.score,
#             'read_time': 1,
#             'read_time_value': self.read_time_value,
#             'category': self.category,
#             'created_at': process_datetime_to_string(self.created_at),
#         }
#         total_views = 0
#         for a in self.action_counts:
#             total_views += self.action_counts[a]
#         data['total_views'] = total_views
#         if self.read_time_value:
#             data['read_time'] = int(self.read_time_value / 60)
#         data['vocab_items'] = [vi.get_json(user) for vi in self.vocab_items.all()]

#         if self.author:
#             socialaccount = self.author.socialaccount_set.first()
#             data['author'] = {'name': self.author.username}
#             if socialaccount:
#                 data['author']['image'] = socialaccount.extra_data['picture']
#                 data['author']['name'] = socialaccount.extra_data['name']

#         return data
