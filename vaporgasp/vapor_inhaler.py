import os

from ZRLoader import ZRLoader

zrl = ZRLoader('/home/hltcoe/ajansen/discovery/exp/buckeye-T25/matches/')

from vaporgasp.queries import (insert_utterance, insert_pseudoterm,
                               insert_audio_event, insert_annotation,
                               update_utterance)

from lib.database import init_dbconn
from settings import buckeye as settings

dbhost = settings['DB_HOST']
dbname = settings['DB_NAME']

db = init_dbconn(host=dbhost,name=dbname)

pt_to_mongo_id = {}

for docid in zrl.AllUtterances():

    # TODO: Don't hardcode audio path to use BUCKEYE path
    AUDIO_PATH_PREFIX = "/home/hltcoe/ajansen/aren_local/BUCKEYE"
    utterance = {
        # For the BUCKEYE dataset, docid's have the form:
        #   s0401a
        #   s1102b
        # which correspond to the files:
        #   /home/hltcoe/ajansen/aren_local/BUCKEYE/s04/s0401a.wav
        #   /home/hltcoe/ajansen/aren_local/BUCKEYE/s11/s1102b.wav
        'hltcoe_audio_path': os.path.join(AUDIO_PATH_PREFIX, docid[0:3], docid + ".wav")
        }
    utterance_mongo_id = insert_utterance(db, utterance)

    this_utterance_pts = []
    
    for ptid in zrl.PTIDsForUtterance(docid):
        #If we haven't seen this pseudoterm before, insert it
        if not ptid in pt_to_mongo_id:
            pt = {'eng_display': 'pt%s'%ptid,
                  'native_display': 'PT%s'%ptid,
                  'zr_pt_id':ptid}
            mongo_ptid = insert_pseudoterm(db,pt)
            pt_to_mongo_id[ptid] = mongo_ptid
            this_utterance_pts.append(mongo_ptid)
            
        for aeid in zrl.AudioEventIDsForPTID(ptid):
            #Each time we see an audio event, it'll be the first time
            filename,start,end = zrl.AudioEventDataForAEID(aeid)

            ae = { 'start_offset':start,
                   'end_offset':end,
                   'duration':end-start,
                   'zr_pt_id':ptid,
                   'pt_id': pt_to_mongo_id[ptid],
                   'utterance_id': utterance_mongo_id}

            insert_audio_event(db, ae)
            
            print "%s %s %s %s" % (docid, ptid, aeid, zrl.AudioEventDataForAEID(aeid))
    utterance['pts'] = this_utterance_pts
    update_utterance( db, utterance_mongo_id, **utterance)

