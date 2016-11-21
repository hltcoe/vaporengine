import codecs
import os
import sys

from django.core.management.base import BaseCommand, CommandError
from visualizer.models import Corpus

class Command(BaseCommand):
    help = 'Export CTM file for an audio corpus'

    def add_arguments(self, parser):
        parser.add_argument('corpus_name', help='Name of audio corpus')
        parser.add_argument('ctm_file_path', help='Filename for CTM file')
        parser.add_argument('--labeled', help='Only export terms that have been labeled',
                            action='store_true')
    
    def handle(self, *args, **options):
        try:
            corpus = Corpus.objects.get(name=options['corpus_name'])
        except Corpus.DoesNotExist:
            sys.stderr.write('ERROR: Unable to find corpus named "%s"\n' % options['corpus_name'])
            return

        ctm_file = codecs.open(options['ctm_file_path'], 'w', encoding='utf-8')
        for document in corpus.document_set.all()[0:10]:
            print document.audio_identifier
            for audio_fragment in document.audiofragment_set.order_by('start_offset'):
                if not options['labeled'] or audio_fragment.term.label:
                    if audio_fragment.term.label:
                        label = audio_fragment.term.label
                    else:
                        label = 'T%.4d' % audio_fragment.term.zr_term_index
                        
                    ctm_file.write('%s A %.2f %.2f %s\n' % (document.audio_identifier,
                                                            audio_fragment.start_offset / 100.0,
                                                            audio_fragment.duration / 100.0,
                                                            label))
        ctm_file.close()
