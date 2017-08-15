import codecs

from pronounce.models import Phrase, PhraseCorpus

def run():
    pc = PhraseCorpus()
    pc.title = 'Oromo Phrases'
    pc.save()

    for (line_index, line) in enumerate(codecs.open('oromo_phrases.txt', encoding='utf-8')):
        phrase = Phrase()
        phrase.phrase_corpus = pc
        phrase.phrase_index = line_index
        phrase.create_from_line(line)

    pc = PhraseCorpus()
    pc.title = 'Tigrinya Phrases'
    pc.save()

    for (line_index, line) in enumerate(codecs.open('tigrinya_phrases.txt', encoding='utf-8')):
        phrase = Phrase()
        phrase.phrase_corpus = pc
        phrase.phrase_index = line_index
        phrase.create_from_line(line)
