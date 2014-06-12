from __future__ import division

"""Specific code for connecting dynamic wordclouds and vennclouds to vaporviz"""

"""vennclouds need data of the form:
[ { name:'dataset_name',
    tokens:[token dicts],
    num_docs: number_of_documents }
  ...
]

token dict: { token: 'display_token', tf:tf, idf:idf, examples:[examples], ... }
"""

from collections import defaultdict

from bson import ObjectId

from lib.queries import find_pseudoterms, find_utterances



def make_wc_datastructure(db, utterances):
    """
    Take a list of utterances and return the relevant token vectors,
    as needed by the dynamic wordcloud/venncloud code.
    """
    pseudoterm_id_set = set()
    pseudoterm_id_totals = defaultdict(int)
    pseudoterm_id_string_to_audio_event_ids = defaultdict(list)
    pseudoterm_id_string_to_utterance_ids = defaultdict(list)
    tf = defaultdict(int)
    tokens = []
    token_to_pseudoterm_id_strings = defaultdict(list) #for graphemes that line up, these will be lists
    utterance_object_ids = []

    for raw_utt_id in utterances:
        if type(raw_utt_id) in [str, unicode]:
            utt_id = ObjectId(raw_utt_id)
        elif type(raw_utt_id) == ObjectId:
            utt_id = raw_utt_id
        else:
            raise TypeError("raw_utt_id type was: '%s'" % type(raw_utt_id))
        utterance_object_ids.append(utt_id)

    utterances_cursor = db.utterances.find({"_id": {"$in": utterance_object_ids}})
    for utterance in utterances_cursor:
        for pseudoterm_id in utterance['pts']:
            pseudoterm_id_set.add(pseudoterm_id)
            pseudoterm_id_totals[pseudoterm_id] += 1
            pseudoterm_id_string_to_utterance_ids[str(pseudoterm_id)].append(utterance['_id'])
    pseudoterm_object_ids = list(pseudoterm_id_set)

    pseudoterms_cursor = db.pseudoterms.find({"_id": {"$in": pseudoterm_object_ids}})
    for pseudoterm in pseudoterms_cursor:
        if 'is_junk' not in pseudoterm or not pseudoterm['is_junk']:
            token = pseudoterm['eng_display']
            tf[token] = pseudoterm_id_totals[pseudoterm['_id']]
            tokens.append(token)
            token_to_pseudoterm_id_strings[token].append(str(pseudoterm['_id']))

    audio_events_cursor = db.audio_events.find({
        "pt_id": {"$in": pseudoterm_object_ids},
        "utterance_id": {"$in": utterance_object_ids}
    })
    for audio_event in audio_events_cursor:
        pseudoterm_id_string_to_audio_event_ids[str(audio_event['pt_id'])].append(audio_event['_id'])

    #Have to get idf somehow to include. For now everything is 1

    #Figure out the right way to integrate dynamic wordcloud package internal calls

    #Now finally make the token feature vector
    token_vector = []
    for token, pseudoterm_id_strings in sorted(token_to_pseudoterm_id_strings.items()):
        audio_event_id_strings_for_token = []
        utterance_id_strings_for_token = []
        for pseudoterm_id_string in pseudoterm_id_strings:
            for audio_event_id in pseudoterm_id_string_to_audio_event_ids[pseudoterm_id_string]:
                audio_event_id_strings_for_token.append(str(audio_event_id))
            for utterance_id in pseudoterm_id_string_to_utterance_ids[pseudoterm_id_string]:
                utterance_id_strings_for_token.append(str(utterance_id))
        t = {
            'audio_event_ids':audio_event_id_strings_for_token,
            'examples':[],
            'idf':1,  #TODO fix IDF
            'number_of_pts':len(pseudoterm_id_strings),
            'pt_ids':pseudoterm_id_strings,
            'text':token,
            'tf':tf[token],
            'utterance_ids':utterance_id_strings_for_token
        }
        token_vector.append(t)

    return token_vector
