import codecs
import json

from visualizer.models import Corpus, Document

def run():
    dd_file = codecs.open('document_durations.json', 'r', encoding='utf-8')
    data = json.loads(dd_file.read())
    dd_file.close()

    for corpus_name in data:
        print "Restoring Document durations for Corpus '%s'" % corpus_name
        corpus = Corpus.objects.filter(name=corpus_name).first()
        for document_audio_identifier in data[corpus_name]:
            document = corpus.document_set.filter(audio_identifier=document_audio_identifier).first()
            document.duration = data[corpus_name][document_audio_identifier]
            document.save()
