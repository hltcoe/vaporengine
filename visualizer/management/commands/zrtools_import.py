import os

from django.core.management.base import BaseCommand, CommandError
import pysox
from visualizer.models import Corpus

class Command(BaseCommand):
    help = 'Import ZRTools output for an audio corpus'

    def add_arguments(self, parser):
        parser.add_argument('corpus_name', help='Name to give to audio corpus')
        parser.add_argument('corpus_path', help='Path to ZRTools output directory')
        parser.add_argument('--audio_directory',
                            help="Directory containing audio files listed in 'files.lst'",
                            default=None)
        parser.add_argument('--audio_extension',
                            help="File extension of audio files listed in CTM 'files.lst' (e.g. 'wav' or 'flac')",
                            default=None)
    
    def handle(self, *args, **options):
        audiofragments_path = os.path.join(options['corpus_path'], 'matches/master_graph.nodes')
        clusters_path = os.path.join(options['corpus_path'], 'matches/master_graph.dedups')
        filenames_path = os.path.join(options['corpus_path'], 'files.lst')

        if not os.path.isfile(audiofragments_path):
            raise CommandError('Cannot find nodes file "%s"' % audiofragments_path)
        if not os.path.isfile(clusters_path):
            raise CommandError('Cannot find clusters file "%s"' % clusters_path)
        if not os.path.isfile(filenames_path):
            raise CommandError('Cannot find filename list file "%s"' % filenames_path)

        first_audio_filename = open(filenames_path, 'r').readline().strip()
        if options['audio_directory']:
            first_audio_filename = os.path.join(options['audio_directory'], os.path.basename(first_audio_filename))
        if options['audio_extension']:
            first_audio_filename += "." + options['audio_extension']

        if not os.path.isfile(first_audio_filename):
            raise CommandError('Cannot find audio file "%s" listed on first line of file "%s"' % \
                               (first_audio_filename, filenames_path))

        try:
            audio = pysox.CSoxStream(first_audio_filename)
        except IOError as e:
            raise CommandError('Unable to read audio data from file "%s": %s' % \
                               (first_audio_filename, e))
        signal_info = audio.get_signal().get_signalinfo()

        corpus = Corpus()
        corpus.create_from_zr_output(
            corpus_name=options['corpus_name'],
            audiofragments=audiofragments_path,
            clusters=clusters_path,
            filenames=filenames_path,
            audio_rate=signal_info['rate'],
            audio_channels=signal_info['channels'],
            audio_precision=signal_info['precision'],
            audio_directory=options['audio_directory'],
            audio_extension=options['audio_extension'])
        corpus.save()
