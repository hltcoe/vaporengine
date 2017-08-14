# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from pronounce.models import Phrase, PhraseCorpus, PhrasePresentation


def index(request):
    context = {
        'phrase_corpora': PhraseCorpus.objects.all()
    }
    return render(request, 'index.html', context)

def phrase(request, phrase_corpus_id, phrase_id):
    phrase_corpus = PhraseCorpus.objects.get(id=phrase_corpus_id)
    phrase = Phrase.objects.get(id=phrase_id)

    last_phrase_index = phrase_corpus.phrase_set.order_by('phrase_index').last().phrase_index
    if phrase.phrase_index == 0:
        previous_phrase_index = last_phrase_index
    else:
        previous_phrase_index = phrase.phrase_index - 1
    previous_phrase_id = phrase_corpus.phrase_set.filter(phrase_index=previous_phrase_index).first().id

    if phrase.phrase_index == last_phrase_index:
        next_phrase_index = 0
    else:
        next_phrase_index = phrase.phrase_index + 1
    next_phrase_id = phrase_corpus.phrase_set.filter(phrase_index=next_phrase_index).first().id

    # Record when phrase was presented to the user
    pp = PhrasePresentation()
    pp.phrase = phrase
    pp.save()
    
    context = {
        'phrase': phrase,
        'phrase_corpus_id': phrase_corpus_id,
        'phrase_id': phrase_id,
        'next_phrase_id': next_phrase_id,
        'previous_phrase_id': previous_phrase_id,
    }
    return render(request, 'phrase.html', context)
