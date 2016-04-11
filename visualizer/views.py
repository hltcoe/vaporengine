import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import pysox
import ujson as json

from visualizer.models import Corpus, Document


def cloud_data_from_utterances(request):
    # TODO: Rename this function while refactoring
    request_data = json.loads(request.body) # Should have a 'dataset' and an 'utterances' field
    print "<<<%s>>>" % request_data

    first_document_id = int(request_data['utterances'][0])
    document = Document.objects.get(id=first_document_id)

    # Sample JSON for Token Vector:
    #   [
    #     {'tf': 2, 'utterance_ids': ['55e5b892841fd54738fcf336', '55e5b892841fd54738fcf336'], 'text': u'pt10525', 'examples': [], 'audio_event_ids': ['55e5b895841fd54738fd3ecd', '55e5b895841fd54738fd3ecf'], 'idf': 1, 'pt_ids': ['55e5b892841fd54738fcf35e'], 'number_of_pts': 1},
    #     {'tf': 1, 'utterance_ids': ['55e5b892841fd54738fcf336'], 'text': u'pt1285', 'examples': [], 'audio_event_ids': ['55e5b895841fd54738fd3e20'], 'idf': 1, 'pt_ids': ['55e5b892841fd54738fcf344'], 'number_of_pts': 1},
    #     {'tf': 1, 'utterance_ids': ['55e5b892841fd54738fcf336'], 'text': u'pt12890', 'examples': [], 'audio_event_ids': ['55e5b895841fd54738fd3ed2'], 'idf': 1, 'pt_ids': ['55e5b892841fd54738fcf35f'], 'number_of_pts': 1}]
    token_vector = []
    for term in document.associated_terms():
        # TODO: Correctly implement TF and IDF measures
        t = {
            'audio_event_ids':term.audio_fragment_ids(),
            'examples':[],
            'idf':1,
            'number_of_pts':1,
            'pt_ids':[term.id],
            'text':term.eng_display,
            'tf':term.total_audio_fragments(),
            'utterance_ids':term.document_ids(),
        }
        token_vector.append(t)

    # TODO: For some reason, JsonResponse complains that arrays cannot
    # be serialized, even when the safe flag is set to False
#    return JsonResponse(token_vector, safe=False)

    response = HttpResponse(content=json.dumps(token_vector))
    response['Content-Type'] = 'application/json'
    return response

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
