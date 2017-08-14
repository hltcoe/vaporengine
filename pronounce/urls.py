from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^phrase/(?P<phrase_corpus_id>\d+)/(?P<phrase_id>\d+)', views.phrase, name='phrase'),
]
