from __future__ import print_function

from datetime import datetime

from pytz import timezone

from pronounce.models import Phrase, PhraseCorpus, PhrasePresentation


def run():
    pc = PhraseCorpus.objects.get(title='Tigrinya Phrases')
    pps = PhrasePresentation.objects.filter(phrase__phrase_corpus=pc).order_by('updated_at')

    # t0 = 2017-08-15 10:10am EDT
    t0 = datetime(2017, 8, 15, 18, 40, 0, 0, tzinfo=timezone('UTC'))

    for (i, pp) in enumerate(pps):
        if i < len(pps)-1:
            start_offset = (pp.updated_at - t0).seconds
            # End offset is the start offset of the next segment
            end_offset = (pps[i+1].updated_at - t0).seconds
            print('%s\t%s\t%d\t%d' % (pp.phrase.utterance_identifier,
                                      'IL5-NI4-20170815-1440',
                                      start_offset,
                                      end_offset))
