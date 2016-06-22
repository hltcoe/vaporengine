import os
import tempfile

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import pysox
import ujson as json

from visualizer.models import Corpus, Document, Term


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

def term_as_json(request, corpus_id, term_id):
    # TODO: This function is a hacky shim used while transitioning from MongoDB to Django
    request_data = json.loads(request.body)
    term = Term.objects.get(id=request_data['term_id'])
    term_json = {
        'eng_display': term.eng_display,
        'native_display': term.native_display,
        # TODO: Remove temporary hack of using MongoDB '_id' field to store term ID
        '_id': term.id,
    }
    return JsonResponse(term_json)

def term_audio_fragments_as_json(request, corpus_id, term_id):
    term = Term.objects.get(id=term_id)

    audio_fragments_json = []
    for audio_fragment in term.audiofragment_set.all():
        audio_fragments_json.append({
            'duration': audio_fragment.duration,
            'audio_identifier': audio_fragment.document.audio_identifier,
            'document_id': audio_fragment.document_id,
            'document_index': audio_fragment.document.document_index
        })
    return JsonResponse(audio_fragments_json, safe=False)

def term_update(request, term_id):
    request_data = json.loads(request.body)
    term = Term.objects.get(id=term_id)
    term.eng_display = request_data['eng_display']
    term.save()
    return JsonResponse({})

def term_wav_file(request, corpus_id, term_id):
    corpus = Corpus.objects.get(id=corpus_id)
    term = Term.objects.get(id=term_id)
    sox_signal_info = pysox.CSignalInfo(corpus.audio_rate, corpus.audio_channels, corpus.audio_precision)

    # TODO: Allow number of audio events to be specified as parameter, instead
    #       of hard-coded to 10
    audio_fragments = term.audiofragment_set.all()[:10]

    # Create a temporary directory
    tmp_directory = tempfile.mkdtemp()
    tmp_filename = os.path.join(tmp_directory, 'combined_clips.wav')

    # The first argument to CSoxStream must be a filename with a '.wav' extension.
    #
    # If the output file does not have a '.wav' extension, pysox will raise
    # an "IOError: No such file" exception.
    outfile = pysox.CSoxStream(tmp_filename, 'w', sox_signal_info)

    print "audio_for_term('%s'):" % term.id
    for audio_fragment in audio_fragments:
        START_OFFSET = bytes("%f" % (audio_fragment.start_offset / 100.0))
        DURATION = bytes("%f" % (audio_fragment.duration / 100.0))
        input_filename = audio_fragment.document.audio_path

        print "  [%s] (%d-%d)" % (input_filename, audio_fragment.start_offset, audio_fragment.end_offset)

        infile = pysox.CSoxStream(input_filename)
        chain = pysox.CEffectsChain(infile, outfile)
        chain.add_effect(pysox.CEffect('trim', [START_OFFSET, DURATION]))
        chain.flow_effects()
        infile.close()

    outfile.close()

    # Read in audio data from temporary file
    wav_data = open(tmp_filename, 'rb').read()

    # Clean up temporary files
    os.remove(tmp_filename)
    os.rmdir(tmp_directory)

    response = HttpResponse(content=wav_data)
    response['Content-Type'] = 'audio/wav'
    return response

def wordcloud_json_for_corpus(request, corpus_id):
    corpus = Corpus.objects.get(id=corpus_id)

    terms = []

    for term in corpus.terms():
        terms.append({
            'eng_display': term.eng_display,
            'zr_pt_id': term.zr_pt_id,

            'term_id': term.id,
            'corpus_id': corpus_id,
            'audio_event_ids': term.audio_fragment_ids(),

            'total_audio_fragments': term.total_audio_fragments(),
            'total_documents': term.total_documents()
        })

    response = HttpResponse(content=json.dumps({
        'sort_keys': {
            'total_documents': 'Documents appeared in',
            'total_audio_fragments': 'Occurrences in corpus',
        },
        'terms': terms
    }))
    response['Content-Type'] = 'application/json'
    return response

def wordcloud_json_for_document(request, corpus_id, document_id):
    document = Document.objects.get(id=document_id)

    terms = []
    for term in document.associated_terms():
        terms.append({
            'eng_display': term.eng_display,
            'zr_pt_id': term.zr_pt_id,

            'term_id': term.id,
            'corpus_id': corpus_id,
            'audio_event_ids': term.audio_fragment_ids(),

            'first_start_offset_in_document': term.first_start_offset_in_document(document),
            'total_audio_fragments': term.total_audio_fragments(),
            'total_audio_fragments_in_document': term.total_audio_fragments_in_document(document),
            'total_documents': term.total_documents()
        })

    response = HttpResponse(content=json.dumps({
        'sort_keys': {
            'total_documents': 'Documents appeared in',
            'first_start_offset_in_document': 'First appearance',
            'total_audio_fragments': 'Occurrences in corpus',
            'total_audio_fragments_in_document': 'Occurences in document'
        },
        'terms': terms
    }))
    response['Content-Type'] = 'application/json'
    return response
