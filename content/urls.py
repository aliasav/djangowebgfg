'''Contains all URLs for content app of project
'''
from django.conf.urls import url
from content import views
from content.views import home_view
from content import api

urlpatterns = [

    # home page url
    url(r'^home/$', views.home_view, name="home_view"),

    url(r'^base/$', views.base_view),

    # detail page for word
    url(r'^dictionary/(?P<word>\w+)$', views.word_view),

    # search page
    url(r'^search/$', views.search_view),

    # GET api for vocab item
    # url(r'^_api/v1/dictionary/(?P<word>\w+)$', api.vocab_item_detail),

    # POST api for vocab item
    # url(r'^_api/v1/update/$', api.vocab_item_update),
    url(r'^_api/v1/dictionary/(?P<word>\w+)$', api.VocabItemDetailAPI.as_view()),
    url(r'^_api/v1/update/$', api.VocabItemDetailAPI.as_view()),
]