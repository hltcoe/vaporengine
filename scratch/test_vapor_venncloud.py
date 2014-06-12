
from lib.database import init_dbconn
from settings import settings

db = init_dbconn(name=settings['DB_NAME'],host=settings['DB_HOST'])

from lib.queries import find_pseudoterms, find_utterances

cur = find_utterances(db, count=30)

utts = [utt['_id'] for utt in cur]

from vaporviz.vapor_venncloud import make_wc_datastructure

token_vector = make_wc_datastructure(db, utts)

print token_vector[:3]


