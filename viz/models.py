from django.db import models


class AudioEvent(models.Model):
    corpus = models.ForeignKey('Corpus')
    pt_id = models.ForeignKey('Pseudoterm')
    utterance_id = models.ForeignKey('Utterance')
    duration = models.IntegerField()
    end_offset = models.IntegerField()
    start_offset = models.IntegerField()
    time = models.BigIntegerField()
    zr_pt_id = models.IntegerField()


class Corpus(models.Model):
    name = models.CharField(max_length=100)


class Pseudoterm(models.Model):
    eng_display = models.CharField(max_length=100)
    native_display = models.CharField(max_length=100)
    zr_pt_id = models.IntegerField()


class Utterance(models.Model):
    """
    What Glen calls an "Utterance", Aren calls a "Document"
    """
    corpus = models.ForeignKey('Corpus')
    hltcoe_audio_path = models.CharField(max_length=1024)
    audio_identifier = models.CharField(max_length=100)
    pseudoterms = models.ManyToManyField('Pseudoterm')
