"""Specific code for connecting dynamic wordclouds and vennclouds to vaporviz"""

"""vennclouds need data of the form:
[ { name:'dataset_name',
    tokens:[token dicts],
    num_docs: number_of_documents }
  ...
]

token dict: { token: 'display_token', tf:tf, idf:idf, examples:[examples], ... }
"""

from __future__ import division

from bson import ObjectId

from vaporgasp.queries import find_pseudoterms, find_utterances



def make_wc_datastructure(db, utterances):
    """
    Take a list of utterances and return the relevant token vectors,
    as needed by the dynamic wordcloud/venncloud code.
    """
    pseudoterm_id_set = set()
    tokens = []
    token_to_pseudoterm_ids = {} #for graphemes that line up, these will be lists
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
    pseudoterm_object_ids = list(pseudoterm_id_set)

    pseudoterms_cursor = db.pseudoterms.find({"_id": {"$in": pseudoterm_object_ids}})
    for pseudoterm in pseudoterms_cursor:
        token = pseudoterm['eng_display']
        tokens.append(token)
        token_to_pseudoterm_ids[token] = token_to_pseudoterm_ids.get(token,[]) + [pseudoterm['_id']]

    #Have to get idf somehow to include. For now everything is 1

    #Figure out the right way to integrate dynamic wordcloud package internal calls
    tf = {}
    for token in tokens:
        tf[token] = tf.get(token,0)+1

    #Now finally make the token feature vector
    token_vector = []
    for token, pseudoterm_ids in sorted(token_to_pseudoterm_ids.items()):
        t = {'text':token, 'tf':tf[token], 'idf':1, 'examples':[],
             'number_of_pts':len(pseudoterm_ids), 'pt_ids':pseudoterm_ids} #TODO fix IDF
        #TODO add pseudoterm length here too?
        token_vector.append(t)

    return token_vector
