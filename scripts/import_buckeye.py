import os

from visualizer.models import Corpus

def run():
    corpus_path = os.path.join(os.getenv('HOME'), 'zr_datasets/buckeye-T25/')
    corpus = Corpus()
    corpus.create_from_zr_output(
        corpus_name="Buckeye",
        audiofragments=os.path.join(corpus_path, "matches/master_graph.nodes"),
        clusters=os.path.join(corpus_path, "matches/master_graph.dedups"),
        filenames=os.path.join(corpus_path, "fileswav.lst"),
        audio_rate=16000,
        audio_channels=1,
        audio_precision=16)
    corpus.save()
