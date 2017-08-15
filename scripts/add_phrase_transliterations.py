from __future__ import print_function

import codecs

from pronounce.models import Phrase, PhraseCorpus

def run():
    pc = PhraseCorpus.objects.get(title='Tigrinya Phrases')

    for line in codecs.open('fileorder.translit_tigrinya', encoding='utf-8'):
        utterance_identifier, transliteration = line.strip().split('\t')
        phrases = Phrase.objects.filter(utterance_identifier=utterance_identifier)
        if phrases:
            phrase = phrases[0]
            phrase.transliteration = transliteration
            phrase.save()
