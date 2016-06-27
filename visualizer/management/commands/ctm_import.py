import os

from django.core.management.base import BaseCommand, CommandError
import pysox
from visualizer.models import Corpus

class Command(BaseCommand):
    help = 'Import CTM file for an audio corpus'

    def add_arguments(self, parser):
        parser.add_argument('corpus_name', help='Name to give to audio corpus')
        parser.add_argument('ctm_file_path', help='Path to CTM file')
        parser.add_argument('audio_directory', help='Directory containing audio files listed in CTM file')
        parser.add_argument('audio_extension', help='File extension of audio files listed in CTM file')
    
    def handle(self, *args, **options):
        if not os.path.isfile(options['ctm_file_path']):
            raise CommandError('Cannot find CTM file "%s"' % options['ctm_file_path'])

        corpus = Corpus()
        corpus.create_from_ctm_file(
            corpus_name=options['corpus_name'],
            ctm_file_path=options['ctm_file_path'],
            audio_directory=options['audio_directory'],
            audio_extension=options['audio_extension'])
        corpus.save()
