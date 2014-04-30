import pymongo
import copy

import datetime as dt

from lib.database import gen_date_args

from lib.timestamping import now_to_millis

from bson import ObjectId

###
### Collection Config
###

UTTERANCES_COLL = 'utterances'
PSEUDOTERMS_COLL = 'pseudoterms'
AUDIO_EVENTS_COLL = 'audio_events'
ANNOTATIONS_COLL = 'annotations'

indexes = {
    UTTERANCES_COLL: [
        [('pts',pymongo.ASCENDING)],
        [('eng_labels',pymongo.ASCENDING)]
    ],
    PSEUDOTERMS_COLL: [
        [('eng_display',pymongo.ASCENDING)],
        [('native_display',pymongo.ASCENDING)]
    ],
    AUDIO_EVENTS_COLL: [
        [('duration',pymongo.DESCENDING)],
        [('zr_pt_id',pymongo.ASCENDING)],
        [('pt_id',pymongo.ASCENDING)],
        [('utterance_id',pymongo.ASCENDING)]
    ],
    ANNOTATIONS_COLL: [
        [('ref_obj_id',pymongo.ASCENDING)],
        [('username',pymongo.ASCENDING)],
        [('label',pymongo.ASCENDING)],
        [('annotation_type',pymongo.ASCENDING)],
        [('time',pymongo.DESCENDING)]
    ]
}



###
### Argument Handling
###

object_id_fields = ['_id','pt_id','utterance_id'] #Recast these as ObjectIds automagically
def _find_by_common(collection, fields=None,  count=50,
                    start_date=None, end_date=None,
                    page=0, sort_by=None, exists=None,
                    does_not_exist=None,
                    **kw):
    """A `find` query handling system for the `twitter` collection.

    `start_date` and `end_date` are milliseconds since January 1, 1970. If a
    string is provided for either, a conversion will take place. It can cover
    just about whatever you throw at it, but read the documentation for
    `gen_date_args` for more detail.

    The `count` flag defaults to 50, but you can set it to 0 to have no limit
    applied.

    Paging starts counting pages at 0.
    """
    query_dict = copy.deepcopy(kw)


    #Deal with fields that must exist or not exist
    if exists:
        for exister in exists:
            query_dict[exister]={'$exists':True}

    if does_not_exist:
        for nonexister in does_not_exist:
            query_dict[nonexister]={'$exists':False}
        

    # Arrange fields to optimize index usage
    #TODO: deal with optimizing indices 
    #if source:
    #    query_dict['source'] = source

    date_args = gen_date_args(start_date, end_date)
    if len(date_args.keys()) > 0:
        query_dict['time'] = date_args

    #Cast these properly as ObjectIds
    for obj_id in object_id_fields:
        if obj_id in query_dict:
            query_dict[obj_id] = ObjectId( query_dict[obj_id] )

        
    # Support sorting, run the query
    # NB: Make sure it's indexed before you sort on it!
    #print "Query Dict:", query_dict #DEBUG
    print "Sorting by:", sort_by
    if sort_by:
        db_cursor = collection.find(query_dict, sort=sort_by, limit=count)
    else:
        db_cursor = collection.find(query_dict,limit=count)
    # apply paging 
    #db_cursor.limit(count) # limit(0) = no limit
    db_cursor.skip(page * count)

    print query_dict
    
    return db_cursor



###
### Utterances
###
"""
    Field specification, [* indicates indexed]:
    * pts: [pt1_obj_id, pt2_obj_id, ...] #Mongo Object IDs
    * eng_labels: ["eng_label1", "eng_label2",...]
    hltcoe_audio_path: string, path to audio file on hltcoe system
    <other>_audio_path: string, path to audio file on someone else's system [many possible]
"""


def find_utterances(db, **kwargs):
    """Accepts any keywords that `_find_by_common` accepts and calls
    `_find_by_common` on the utterance collection.
    """
    return _find_by_common(db[UTTERANCES_COLL], **kwargs)

def insert_utterance(db, utterance):
    """ Accepts a dictionary specifiying an entry into the utterance table. """
    print utterance
    utterance_id = db[UTTERANCES_COLL].insert(utterance)
    return utterance_id


def update_utterance(db, utterance_id, **updates):
    """update an utterance entry"""
    match_dict = {'_id':ObjectId(utterance_id)}
    if '_id' in updates: # Mongo doesn't like this and refuses to update if we do this
        del updates['_id']
    update_dict = { '$set': updates}
    print 'updating', match_dict, 'with', update_dict
    db[UTTERANCES_COLL].update(match_dict,update_dict,multi=False)


###
### Pseudoterms
###
"""    
    Field specification, [* indicates indexed]:
    * eng_display: string, the latest English annotated with this file (pt# until annotated)
    * native_display: string, the latest annotation on this file, in the native script
    zr_pt_id: Aren's zero resource ID
    (again, pt# until annotated)
"""

def find_pseudoterms(db, **kwargs):
    """Accepts any keywords that `_find_by_common` accepts and calls
    `_find_by_common` on the pseudoterms collection.
    """
    return _find_by_common(db[PSEUDOTERMS_COLL], **kwargs)

def insert_pseudoterm(db, pseudoterm):
    """ Accepts a dictionary specifiying an entry into the pseudoterm table. """
    print pseudoterm
    pseudoterm_id = db[PSEUDOTERMS_COLL].insert(pseudoterm)
    return pseudoterm_id

def update_pseudoterm(db, pseudoterm_id, **updates):
    """update an pseudoterm entry"""
    match_dict = {'_id':ObjectId(pseudoterm_id)}
    if '_id' in updates: # Mongo doesn't like this and refuses to update if we do this
        del updates['_id']
    update_dict = { '$set': updates}
    print 'updating', match_dict, 'with', update_dict
    db[PSEUDOTERMS_COLL].update(match_dict,update_dict,multi=False)


###
### Audio Events
###
"""
    Field specification, [* indicates indexed]:
    audio_file: utterance_obj_id, indicating which audio file it refers to
    #TODO: optionally, should we include the path here, or is the additional lookup fast enough?
    start_offset: int, in frames
    end_offset: int, in frames
    * duration: int, in frames
    annotations: [annotation1_obj_id, annotation2_obj_id, ...]
    pt_id: mongoID of pseudoterm this refers to
    utterance_id: mongoID of the utterance this PT came from
"""

def find_audio_events(db, **kwargs):
    """Accepts any keywords that `_find_by_common` accepts and calls
    `_find_by_common` on the audio events collection.
    """
    return _find_by_common(db[AUDIO_EVENTS_COLL], **kwargs)

def insert_audio_event(db, audio_event):
    """ Accepts a dictionary specifiying an entry into the audio event table.
    It will auto-generate `time`, everything else should be specified by the caller
    of this function."""
    audio_event['time'] = now_to_millis()
    print audio_event
    audio_event_id = db[AUDIO_EVENTS_COLL].insert(audio_event)
    return audio_event_id


###
### Annotations
###
"""
    Field specification, [* indicates indexed]:
    * ref_obj_id: BSON Object ID of object this refers to
    status: some not-yet-specified status of the annotation [QCd, etc?]
    * username: string, user making this annotation
    * label: the actual annotation [probably usually a string]
    comment: string, any miscellaneous comments associated with this annotation
    * annotation_type: string, of a small enumerable type
    * time: milliseconds since epoch, the time this annotation was 
"""

def find_annotations(db, **kwargs):
    """Accepts any keywords that `_find_by_common` accepts and calls
    `_find_by_common` on the annotations collection.
    """
    return _find_by_common(db[ANNOTATIONS_COLL], **kwargs)

def insert_annotation(db, annotation):
    """ Accepts a dictionary specifiying an entry into the annotation table.
    It will auto-generate `time`, everything else should be specified by the caller
    of this function.
    Returns the ID returned by Mongo"""
    annotation['time'] = now_to_millis()
    print annotation
    annotation_id = db[ANNOTATIONS_COLL].insert(annotation)
    return annotation_id
    
def update_annotation(db, annotation_id, **updates):
    """update an pseudoterm entry"""
    match_dict = {'_id':ObjectId(pseudoterm_id)}
    if '_id' in updates: # Mongo doesn't like this and refuses to update if we do this
        del updates['_id']
    update_dict = { '$set': updates}
    print 'updating', match_dict, 'with', update_dict
    db[ANNOTATIONS_COLL].update(match_dict,update_dict,multi=False)






