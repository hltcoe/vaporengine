import os

from visualizer.models import Corpus

def run():
    corpus_path = os.path.join(os.getenv('HOME'), 'zr_datasets/buckeye-T25/')
    corpus = Corpus()
    corpus.create_from_zr_output(
        "Buckeye",
        os.path.join(corpus_path, "matches/master_graph.nodes"),
        os.path.join(corpus_path, "matches/master_graph.dedups"),
        os.path.join(corpus_path, "fileswav.lst"),
        16000, 1, 16)
    corpus.save()
