
#from settings import settings
from lib.database import init_dbconn, init_apply_all_indexes
from lib.queries import *


db = init_dbconn()



returned = update_utterance( db,
                             "5360d12904dc07044277d7b8",
                             **{'dummy_field': 123123123123})


print returned
