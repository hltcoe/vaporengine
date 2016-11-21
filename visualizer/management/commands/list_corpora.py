import codecs
import os

from django.core.management.base import BaseCommand, CommandError
from visualizer.models import Corpus

class Command(BaseCommand):
    help = 'Print out list of available corpora'

    def handle(self, *args, **options):
        for corpus in Corpus.objects.all():
            print '%s' % corpus.name
