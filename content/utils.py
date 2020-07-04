from content.models import VocabItem
import requests


class FetchDict():
    '''calls dict api for a word'''
    def __init__(self, word):
        self.word = word
        self.url = ''
    
    def fetch_word(self):
        pass

    def save_to_db(self, word_dict):
        '''saves word to database
        '''
        # check - filter
        VocabItem.objects.create(**word_dict)


def download_all_words(words):

    '''
    [{'word': '', meaning: ''}, ]
    '''
    for word in words:
        w = word.get('word')
        vocab_item_qset = VocabItem.objects.filter(word=w)
        # if qset is empty: create a new obj
        # update obj: save method

        if not vocab_item_qset:            
            # create word in db
            VocabItem.objects.create()
        else:
            # update an existing object
            obj = vocab_item_qset[0]
            obj.meaning = word.get('meaning')
            obj.save() # save method

