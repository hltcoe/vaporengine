import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import pysox
import ujson as json

from visualizer.models import Corpus, Document


def corpus_wordcloud(request, corpus_id):
    corpus = Corpus.objects.get(id=corpus_id)
    context = {'corpus': corpus}
    return render(request, "corpus_wordcloud.html", context)

def corpus_document_list(request, corpus_id):
    corpus = Corpus.objects.get(id=corpus_id)
    document_list = corpus.document_set.all()
    context = {'corpus': corpus, 'document_list': document_list}
    return render(request, "corpus_document_list.html", context)

def document(request, corpus_id, document_id):
    corpus = Corpus.objects.get(id=corpus_id)
    document = Document.objects.get(id=document_id)
    terms = document.associated_terms()
    audio_fragments = document.audiofragment_set.all()
    context = {
        'corpus': corpus,
        'document': document,
        'terms': terms,
        'audio_fragments': audio_fragments,
    }
    return render(request, "document.html", context)

def document_wav_file(request, corpus_id, document_id):
    document = Document.objects.get(id=document_id)
    audio_file = open(document.audio_path, 'rb')
    response = HttpResponse(content=audio_file)
    response['Content-Type'] = 'audio/wav'
    return response

def index(request):
    current_corpora = Corpus.objects.all()
    context = {'current_corpora': current_corpora}
    return render(request, "index.html", context)

#    pysox.CSoxInfo(corpus.audio_rate, corpus.audio_channels, corpus.audio_precision)


