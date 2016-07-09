import collections
import json
import os
import tempfile

from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
import pysox

from visualizer.models import AudioFragment, Corpus, Document, Term


def corpus_wordcloud(request, corpus_id):
    corpus = Corpus.objects.get(id=corpus_id)
    if corpus.protected_corpus and not request.user.is_authenticated():
        return redirect('/login/?next='+request.path)
    context = {'corpus': corpus}
    return render(request, "corpus_wordcloud.html", context)

def corpus_document_list(request, corpus_id):
    corpus = Corpus.objects.get(id=corpus_id)
    if corpus.protected_corpus and not request.user.is_authenticated():
        return redirect('/login/?next='+request.path)
    document_list = corpus.document_set.all()
    context = {'corpus': corpus, 'document_list': document_list}
    return render(request, "corpus_document_list.html", context)

def document(request, corpus_id, document_id):
    corpus = Corpus.objects.get(id=corpus_id)
    if corpus.protected_corpus and not request.user.is_authenticated():
        return redirect('/login/?next='+request.path)
    context = {
        'corpus_id': corpus_id,
        'document_id': document_id,
    }
    return render(request, "document.html", context)

def document_audio_fragments_as_json(request, corpus_id, document_id):
    document = Document.objects.get(id=document_id)
    audio_fragments_json = []
    for audio_fragment in document.audiofragment_set.all():
        audio_fragments_json.append({
            'audio_fragment_id': audio_fragment.id,
            'start_offset': audio_fragment.start_offset,
            'end_offset': audio_fragment.end_offset
        })
    return JsonResponse(audio_fragments_json, safe=False)

def document_wav_file(request, corpus_id, document_id):
    document = Document.objects.get(id=document_id)
    if os.path.splitext(document.audio_path)[1] == '.wav':
        audio_file = open(document.audio_path, 'rb')
        response = HttpResponse(content=audio_file)
    else:
        # Convert non-WAV files to WAV files using pysox
        tmp_directory = tempfile.mkdtemp()
        tmp_filename = os.path.join(tmp_directory, 'converted.wav')

        infile = pysox.CSoxStream(document.audio_path)
        outfile = pysox.CSoxStream(tmp_filename, 'w', infile.get_signal())
        chain = pysox.CEffectsChain(infile, outfile)
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

def index(request):
    current_corpora = Corpus.objects.all()
    context = {'current_corpora': current_corpora}
    return render(request, "index.html", context)

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

@csrf_exempt
def term_update(request, term_id):
    request_data = json.loads(request.body)
    term = Term.objects.get(id=term_id)
    term.label = request_data['label']
    term.save()
    return JsonResponse({})

def term_wav_file(request, corpus_id, term_id):
    corpus = Corpus.objects.get(id=corpus_id)
    term = Term.objects.get(id=term_id)
    sox_signal_info = pysox.CSignalInfo(corpus.audio_rate, corpus.audio_channels, corpus.audio_precision)

    # TODO: Allow number of audio fragments to be specified as parameter, instead
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

    # Use Django's annotate() to compute total # of Documents and AudioFragments associated with each Term.
    #
    # With annotate(), we can compute the # of AudioFragments associated with each Term in a Corpus using
    # just a single SQL query for the entire Corpus.  This is an order-of-magnitude faster than making
    # a separate SQL call for each Term in the Corpus by calling term.total_audio_fragments() in a for loop.
    terms = corpus.terms().annotate(Count('audiofragment'), Count('audiofragment__document', distinct=True))

    # Create a mapping from each Term ID to the corresponding list of AudioFragment IDs, using a single SQL query.
    #
    # This is an order of magnitude faster than using a separate SQL query for each Term by calling
    # term.audio_fragment_ids() in a for loop.
    term_audiofragment_id_pairs = AudioFragment.objects.filter(document__corpus_id=corpus_id).values_list('term_id', 'id')
    term_id_to_audiofragment_ids = collections.defaultdict(list)
    for (term_id, audiofragment_id) in term_audiofragment_id_pairs:
        term_id_to_audiofragment_ids[term_id].append(audiofragment_id)

    terms_json = []
    for term in terms:
        terms_json.append({
            'label': term.label,
            'zr_term_index': term.zr_term_index,

            'term_id': term.id,
            'corpus_id': corpus_id,

            'audio_fragment_ids': term_id_to_audiofragment_ids[term.id],
            'total_audio_fragments': term.audiofragment__count,
            'total_documents': term.audiofragment__document__count,
        })
    default_sort_key = 'label'
    terms_json = sorted(terms_json, key=lambda k: k[default_sort_key])
    response = HttpResponse(content=json.dumps({
        'default_size_key': 'total_documents',
        'size_keys': [
            {'key_name': 'total_documents', 'key_description': 'Documents appeared in'},
            {'key_name': 'total_audio_fragments', 'key_description': 'Occurrences in corpus'},
        ],
        'default_sort_key': default_sort_key,
        'sort_keys': [
            {'key_name': 'total_documents', 'key_description': 'Documents appeared in'},
            {'key_name': 'label', 'key_description': 'Label'},
            {'key_name': 'total_audio_fragments', 'key_description': 'Occurrences in corpus'}
        ],
        'terms': terms_json
    }))
    response['Content-Type'] = 'application/json'
    return response

def wordcloud_json_for_document(request, corpus_id, document_id):
    corpus = Corpus.objects.get(id=corpus_id)
    document = Document.objects.get(id=document_id)

    terms = document.associated_terms().annotate(audio_fragments_in_document=Count('audiofragment', distinct=True))

    # Create a mapping from Term ID to # of Documents Term appears in, using a single SQL query
    term_id_and_document_counts = corpus.terms().annotate(document_count=Count('audiofragment__document', distinct=True)).values_list('id', 'document_count')
    term_id_to_document_count = {}
    for (term_id, document_count) in term_id_and_document_counts:
        term_id_to_document_count[term_id] = document_count

    # Create a mapping from each Term ID to the corresponding list of AudioFragment IDs, using a single SQL query.
    term_audiofragment_id_pairs = AudioFragment.objects.filter(document__corpus_id=corpus_id).values_list('term_id', 'id')
    term_id_to_audiofragment_ids = collections.defaultdict(list)
    for (term_id, audiofragment_id) in term_audiofragment_id_pairs:
        term_id_to_audiofragment_ids[term_id].append(audiofragment_id)

    terms_json = []
    for term in terms:
        terms_json.append({
            'label': term.label,
            'zr_term_index': term.zr_term_index,

            'term_id': term.id,
            'corpus_id': corpus_id,

            'audio_fragment_ids': term_id_to_audiofragment_ids[term.id],
            'first_start_offset_in_document': term.first_start_offset_in_document(document),
            'total_audio_fragments': len(term_id_to_audiofragment_ids[term.id]),
            'total_audio_fragments_in_document': term.audio_fragments_in_document,
            'total_documents': term_id_to_document_count[term.id],
        })
    default_sort_key = 'first_start_offset_in_document'
    terms_json = sorted(terms_json, key=lambda k: k[default_sort_key])
    response = HttpResponse(content=json.dumps({
        'default_size_key': 'total_documents',
        'size_keys': [
            {'key_name': 'total_documents', 'key_description': 'Documents appeared in'},
            {'key_name': 'total_audio_fragments', 'key_description': 'Occurrences in corpus'},
            {'key_name': 'total_audio_fragments_in_document', 'key_description': 'Occurences in document'}
        ],
        'default_sort_key': default_sort_key,
        'sort_keys': [
            {'key_name': 'total_documents', 'key_description': 'Documents appeared in'},
            {'key_name': 'first_start_offset_in_document', 'key_description': 'First appearance'},
            {'key_name': 'label', 'key_description': 'Label'},
            {'key_name': 'total_audio_fragments', 'key_description': 'Occurrences in corpus'},
            {'key_name': 'total_audio_fragments_in_document', 'key_description': 'Occurences in document'}
        ],
        'terms': terms_json
    }))
    response['Content-Type'] = 'application/json'
    return response
