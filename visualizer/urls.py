from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cloud_data_from_utterances', views.cloud_data_from_utterances, name='cloud_data_from_utterances'),
    url(r'^(?P<corpus_id>\d+)/document/(?P<document_id>\d+)/', views.document, name='document'),
    url(r'^(?P<corpus_id>\d+)/document/list/', views.corpus_document_list, name='corpus_document_list'),
    url(r'^(?P<corpus_id>\d+)/document/(?P<document_id>\d+).wav', views.document_wav_file, name='document_wav_file'),
    url(r'^(?P<corpus_id>\d+)/term/(?P<term_id>\d+).wav', views.term_wav_file, name='term_wav_file'),
    url(r'^(?P<corpus_id>\d+)/term/(?P<term_id>\d+).json', views.term_as_json, name='term_as_json'),
    url(r'^(?P<corpus_id>\d+)/term/(?P<term_id>\d+)_audio_fragments.json',
        views.term_audio_fragments_as_json, name='term_audio_fragments_as_json'),
    url(r'^(?P<corpus_id>\d+)/wordcloud/', views.corpus_wordcloud, name='corpus_wordcloud'),
]
