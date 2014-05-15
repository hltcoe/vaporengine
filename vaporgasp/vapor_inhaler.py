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

zrl = ZRLoader(settings['ZRL_PATH'])


ae_to_mongo_id = {}
pt_to_mongo_id = {}

for utterance in zrl.AllUtterances():
    utterance_fields = {
        'hltcoe_audio_path': zrl.filename_for_utterance[utterance]
        }
    utterance_mongo_id = insert_utterance(db, utterance_fields)

    this_utterance_pts = []
    
    for ptid in zrl.PTIDsForUtterance(utterance):
        # If we haven't seen this pseudoterm before, insert it
        if not ptid in pt_to_mongo_id:
            pt = {'eng_display': 'pt%s'%ptid,
                  'native_display': 'PT%s'%ptid,
                  'zr_pt_id':ptid}
            mongo_ptid = insert_pseudoterm(db,pt)
            pt_to_mongo_id[ptid] = mongo_ptid
        mongo_ptid = pt_to_mongo_id[ptid]
        this_utterance_pts.append(mongo_ptid)
            
        for aeid in zrl.AudioEventIDsForPTID(ptid):
            if not aeid in ae_to_mongo_id:
                filename,start,end = zrl.AudioEventDataForAEID(aeid)

                ae = { 'start_offset':start,
                       'end_offset':end,
                       'duration':end-start,
                       'zr_pt_id':ptid,
                       'pt_id': pt_to_mongo_id[ptid],
                       'utterance_id': utterance_mongo_id}

                mongo_aeid = insert_audio_event(db, ae)
                ae_to_mongo_id[aeid] = mongo_aeid
            
            #print "%s %s %s %s" % (utterance, ptid, aeid, zrl.AudioEventDataForAEID(aeid))

    utterance_fields['pts'] = this_utterance_pts
    print "Pseudoterms for utterance",utterance_mongo_id,":", utterance_fields['pts']
    print utterance_fields.keys()
    update_utterance( db, utterance_mongo_id, **utterance_fields)
