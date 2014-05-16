import os

from ZRLoader import ZRLoader

from vaporgasp.queries import (insert_utterance, insert_pseudoterm,
                               insert_audio_event, insert_annotation,
                               update_utterance)

from lib.database import init_dbconn
from settings import buckeye as settings


dbhost = settings['DB_HOST']
dbname = settings['DB_NAME']

db = init_dbconn(host=dbhost,name=dbname)

zrl = ZRLoader(settings['ZRL_PATH'], clusters=settings['ZRL_CLUSTERS'])


audioevent_to_mongo_id = {}
pseudoterm_to_mongo_id = {}
utterance_to_mongo_id = {}

for utterance in zrl.AllUtterances():
    utterance_fields = {
        'hltcoe_audio_path': zrl.filename_for_utterance[utterance]
        }
    utterance_mongo_id = insert_utterance(db, utterance_fields)
    utterance_to_mongo_id[utterance] = utterance_mongo_id

    this_utterance_pts = []
    for pseudoterm_id in zrl.PTIDsForUtterance(utterance):
        # If we haven't seen this pseudoterm before, insert it
        if not pseudoterm_id in pseudoterm_to_mongo_id:
            pt = {'eng_display': 'pt%s'%pseudoterm_id,
                  'native_display': 'PT%s'%pseudoterm_id,
                  'zr_pt_id':pseudoterm_id}
            mongo_pseudoterm_id = insert_pseudoterm(db,pt)
            pseudoterm_to_mongo_id[pseudoterm_id] = mongo_pseudoterm_id
        mongo_pseudoterm_id = pseudoterm_to_mongo_id[pseudoterm_id]
        this_utterance_pts.append(mongo_pseudoterm_id)

    utterance_fields['pts'] = this_utterance_pts
    print "Pseudoterms for utterance", utterance_mongo_id, ":", utterance_fields['pts']
    print utterance_fields.keys()
    update_utterance(db, utterance_mongo_id, **utterance_fields)

for utterance in zrl.AllUtterances():
    for pseudoterm_id in zrl.PTIDsForUtterance(utterance):
        for audioevent_id in zrl.AudioEventIDsForPTID(pseudoterm_id):
            if not audioevent_id in audioevent_to_mongo_id:
                utterance,start,end = zrl.AudioEventDataForAEID(audioevent_id)

                ae = { 'start_offset': start,
                       'end_offset': end,
                       'duration': end-start,
                       'zr_pt_id': pseudoterm_id,
                       'pt_id': pseudoterm_to_mongo_id[pseudoterm_id],
                       'utterance_id': utterance_to_mongo_id[utterance]}

                mongo_audioevent_id = insert_audio_event(db, ae)
                audioevent_to_mongo_id[audioevent_id] = mongo_audioevent_id
