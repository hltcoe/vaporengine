import codecs
import os

from visualizer.models import Corpus, Document, DocumentTopic

def run():
    corpus = Corpus.objects.get(name=u"Turkish")

    # Topic file is a TSV file with a header line, with the format:
    #   filename        topic
    #   BN_CRI_TUR_audio00001_20140722.flac     Civil Unrest
    #   BN_CRI_TUR_audio00002_20140804.flac     Earthquake
    #   BN_CRI_TUR_audio00003_20141202.flac     Health
    topic_file = os.path.join(os.getenv("HOME"), "zr_datasets/turkish/audio_topics.txt")
    topic_lines = codecs.open(topic_file, encoding="utf-8").readlines()

    for topic_line in topic_lines[1:]:
        (filename, label) = topic_line.strip().split('\t')
        audio_identifier = os.path.splitext(filename)[0]
        document = Document.objects.get(audio_identifier=audio_identifier)
        (document_topic, _) = DocumentTopic.objects.get_or_create(corpus=corpus, label=label)
        document_topic.documents.add(document)
