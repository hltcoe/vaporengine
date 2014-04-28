import pymongo

import datetime as dt

###
### Index Handling
###

def init_apply_all_indexes(indexes):
    """A closure around indexes to simplify applying them to the data
    unique to any session, eg. database and collection.

    The returned function applies all configured indexes for a collection.
    Intended for use after functions that create/update/delete entire
    documents.
    """
    def apply_all_indexes(db, collection):
        if collection not in indexes:
            raise ValueError("Collection does not have indexes defined")
        for index in indexes[collection]:
            db[collection].ensure_index(index)
    return apply_all_indexes


###
### Collection Config
###

UTTERANCE_COLL = 'utterances'
PSEUDOTERMS_COLL = 'pseudoterms'
AUDIO_EVENT_COLL = 'audio_events'
ANNOTATION_COLL = 'annotations'

indexes = {
    ## Indexes for the email collection
    UTTERANCE_COLL: [
        [('pts',pymongo.ASCENDING)]
    ],
    PSEUDOTERMS_COLL: [
        [('audio_events',pymongo.ASCENDING)],
        [('eng_display',pymongo.ASCENDING)],
        [('native_display',pymongo.ASCENDING)]
    ],
    AUDIO_EVENT_COLL: [
        [('duration',pymongo.DESCENDING)]
    ],
    ANNOTATION_COLL: [
        [('ref_obj_id',pymongo.ASCENDING)],
        [('username',pymongo.ASCENDING)],
        [('label',pymongo.ASCENDING)],
        [('annotation_type',pymongo.ASCENDING)],
        [('time',pymongo.DESCENDING)]
    ]
}


from time import mktime
from datetime import datetime
from dateutil.parser import parse


###
### Converstion Helpers
###

def datestring_to_millis(ds):
    """Takes a string representing the date and converts it to milliseconds
    since epoch.
    """
    dt = parse(ds)
    return datetime_to_millis(dt)

def datetime_to_millis(dt):
    """Takes a datetime instances and converts it to milliseconds since epoch.
    """
    seconds = dt.timetuple()
    seconds_from_epoch = mktime(seconds)
    return seconds_from_epoch * 1000 # milliseconds

def millis_to_datetime(ms):
    """Converts milliseconds into it's datetime equivalent
    """
    seconds = ms / 1000.0
    return datetime.fromtimestamp(seconds)


###
### Argument Handling
###

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
    * pts: [pt1_obj_id, pt2_obj_id, ...]
    annotations: [annotation1_obj_id, annotation2_obj_id, ...]
    hltcoe_audio_path: string, path to audio file on hltcoe system
    <other>_audio_path: string, path to audio file on someone else's system [many possible]
"""


def find_utterances(db, **kwargs):
    """Accepts any keywords that `_find_by_common` accepts and calls
    `_find_by_common` on the utterance collection.
    """
    return _find_by_common(db[UTTERANCE_COLL], **kwargs)

def insert_utterance(db, utterance):
    """ Accepts a dictionary specifiying an entry into the utterance table. """
    print utterance
    utterance_id = db[UTTERANCE_COLL].insert(utterance)
    return utterance_id



###
### Pseudoterms
###
"""    
    Field specification, [* indicates indexed]:
    * audio_events: [ae1_obj_id, ae2_obj_id, ...]
    annotations: [annotation1_obj_id, annotation2_obj_id, ...]
    * eng_display: string, the latest English annotated with this file (pt# until annotated)
    * native_display: string, the latest annotation on this file, in the native script
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
    pseudoterm_id = db[PSEUDOTERM_COLL].insert(pseudoterm)
    return pseudoterm_id



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
    audio_event_id = db[AUDIO_EVENT_COLL].insert(audio_event)
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

def insert_annotations(db, annotation):
    """ Accepts a dictionary specifiying an entry into the annotation table.
    It will auto-generate `time`, everything else should be specified by the caller
    of this function.
    Returns the ID returned by Mongo"""
    annotation['time'] = now_to_millis()
    print annotation
    annotation_id = db[ANNOTATION_COLL].insert(annotation)
    return annotation_id
    






