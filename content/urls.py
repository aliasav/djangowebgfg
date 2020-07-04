'''
Contains all URLs for content app of project
'''
from django.conf.urls import url
from content import views as content_views

urlpatterns = [

    # home page url
    url(r'^home/$', content_views.home_view),

    url(r'^base/$', content_views.base_view),
    
    # /dictionary/<word>
    url(r'^dictionary/(?P<word>\w+)$', content_views.word_view),
]
