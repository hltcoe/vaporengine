# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class PhraseCorpus(models.Model):
    title = models.TextField()

class Phrase(models.Model):
    phrase_corpus = models.ForeignKey(PhraseCorpus)
    
    utterance_identifier = models.TextField(db_index=True)
    phrase_index = models.IntegerField()
    phrase_text = models.TextField()
    transliteration = models.TextField(null=True)

    def create_from_line(self, line):
        # Input data files have the form:
        #   IL5_set0_monolingual_text_1 ምርጫ ኢትዮጵያ፡ ኣብ ሰለስተ ተወላዶ ትግራይ ዝተፈላለየ ፖሊትካዊ ኣረኣእያ ይፈጥር
        #   IL5_set0_monolingual_text_9 ዩ-ስ ምስ ኢትዮጵያ ንዘለዋ ርክብ ተጠንቂቃ ትሕዞ!
        line = line.strip()
        first_space_index = line.find(' ')
        self.utterance_identifier = line[0:first_space_index]
        self.phrase_text = line[first_space_index+1:]
        self.save()

class PhrasePresentation(models.Model):
    """Records when a Phrase was presented to an NI"""
    phrase = models.ForeignKey(Phrase)
    ip_address = models.TextField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
