
#from settings import buckeye as settings
from lib.database import init_dbconn, init_apply_all_indexes
from vaporgasp.queries import *


db = init_dbconn()

#Test utterances

dummy_utterance = {
    'pts' : ["objid1","objid2"],
    'eng_labels': ['there','are','fools','being','pitied'],
    'hltcoe_audio_path':'/export/projects/vaporengine/blahlbahlbah/lskjdlfkjsdf.wav'
    }

print "Inserting:", insert_utterance(db, dummy_utterance)
print "Finding:", find_utterances(db).next()



#Test pseudoterms

dummy_pseudoterm = {
    'zr_pt_id': 123123,
    'eng_display': 'I pity the fool',
    'native_display': 'ah pity da foo'
    }

print "Inserting:", insert_pseudoterm(db, dummy_pseudoterm)
print "Finding:", find_pseudoterms(db).next()


#Test Audio events

dummy_audio_event = {
    'start_offset': 1234,
    'end_offset':1239,
    'duration':5,
    'zr_pt_id':123123,
    'pt_id':"123234-23423-234234",
    'utterance_id':"23909-2098-23098234"
    }

print "Inserting:", insert_audio_event(db, dummy_audio_event)
print "Finding:", find_audio_events(db).next()


#Test Annotation

dummy_annotation = {
    'ref_obj_id':'bson object id',
    'status':'tired',
    'username':'gac',
    'label':'do you feel lucky, punk?',
    'comment':'well do ya?',
    'annotation_type':'snark'
    }

print "Inserting:", insert_annotation(db, dummy_annotation)
print "Finding:", find_annotations(db).next()



#Test applying indexing
from vaporgasp.queries import indexes
apply_indices = init_apply_all_indexes(indexes)
for collection in indexes.keys():
    apply_indices(db,collection)

print "fin"



