import codecs
import json

from visualizer.models import Corpus, Document

def run():
    data = {}
    
    for corpus in Corpus.objects.all():
        data[corpus.name] = {}
        for document in corpus.document_set.all():
            data[corpus.name][document.audio_identifier] = document.duration

    dd_file = codecs.open('document_durations.json', 'w', encoding='utf-8')
    dd_file.write(json.dumps(data))
    dd_file.close()

    print "Backed up Document durations to 'document_durations.json'"
