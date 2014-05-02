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

#from vaporgasp.queries import (find_pseudoterms_from_eng_label, find_pseudoterms,
from vaporgasp.queries import (find_pseudoterms,
                               find_utterances)

from bson import ObjectId
def make_wc_datastructure(db, utterances ):
    """Take a list of utterances and return the relevant
    token vectors, as needed by the dynamic wordcloud/venncloud code. """

    docs = []

    token_to_mongoids = {} #for graphemes that line up, these will be lists
    mongoid_to_token = {} #So we don't have to pull the same PT multiple times

    #loop through utterances pulling out pseudoterms that occur in them
    for raw_utt_id in utterances:
        if type(raw_utt_id) == type(" "):
            utt_id = ObjectId(raw_utt_id)
        else:
            utt_id = raw_utt_id
        utt = find_utterances(db, _id=utt_id ).next()
        this_doc = []
        #loop through pseudoterms and make a document out of them
        for pt_id in utt['pts']:


            #If we've seen it before, don't hit the DB, just pull out the token
            if pt_id in mongoid_to_token:
                token = mongoid_to_token[pt_id]
            else:
                #If we haven't seen it, hit the DB, add to appropriate places
                pt = find_pseudoterms(db, _id=ObjectId(pt_id)).next()
                token = pt['eng_display']
                token_to_mongoids[token] = token_to_mongoids.get(token,[]) + [pt_id]
                mongoid_to_token[pt_id] = token

            this_doc.append( token )
        docs.append(sorted(this_doc))

    #Have to get idf somehow to include. For now everything is 1

    #Figure out the right way to integrate dynamic wordcloud package internal calls
    tf = {}
    for doc in docs:
        for token in doc:
            tf[token] = tf.get(token,0)+1

    #Now finally make the token feature vector
    token_vector = []
    for token,mongo_ids in sorted(token_to_mongoids.items()):
        t = {'token':token, 'tf':tf[token], 'idf':1, 'examples':[],
             'number_of_pts':len(mongo_ids), 'pt_ids':mongo_ids} #TODO fix IDF
        #TODO add pseudoterm length here too?
        token_vector.append(t)
        
    return token_vector
    
    

