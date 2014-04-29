from bottle import route, run, request, response

import argparse
import datetime as dt

try:
    import ujson as json
except:
    import json

from lib.database import init_dbconn
from vaporgasp.queries import (find_annotations, find_utterances,
                               find_pseudoterms, find_audio_events)
    
# the decorator to ease some javascript pain (if memory serves)
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS, HEAD'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        
        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

def json_wrapper(method):
    def rapper(*a, **kw):
        resp = method(*a, **kw)
        response.content_type = 'application/json'
        return json.dumps(resp)
    return rapper


"""For serving generic widgets and pages"""
@route('/www/<path>')
def widget_handler(path):
    source_path = 'page_source/%s' % path 
    try:
        page = open( source_path ).read()
    except:
        #print "Failing to find", source_path
        source_path = 'vaporviz/'+source_path
        #print "Looking for", source_path
        page = open( source_path ) .read()
    print "Returning what was found at:", source_path
    return page


def generic_find(find_function, metadata_filters):
    """Does all the requisite conversions for pulling from the database
    and preparing to serve to the website.
    `find_function` should be one of the function from queries.py"""
    print metadata_filters
    dataset = metadata_filters['dataset'] #This maps to MongoDB table name
    print "from dataset:", dataset
    del metadata_filters['dataset']

    #SECURITY add whitelist of dataset names permitted
    db = init_dbconn(name = dataset, host='r4n7')

    #Properly Cast count
    if 'count' in metadata_filters:
        try:
            metadata_filters['count'] = int(metadata_filters['count'])
        except:
            metadata_filters['count'] = 0

    #SECURITY -- delete all keys not in a whitelisted set of keys

    sort_by = [('time',-1)]
    if 'sort_by' in metadata_filters:
        sort_by = metadata_filters['sort_by'] #Or do we need a conversion here

    print metadata_filters
    cursor = find_function(db, **metadata_filters)

    #Accumulate results
    results = []
    for result in cursor:
        result['_id'] = str(result['_id'])
        results.append(result)
    print "Results:", results
    return results
    


@route('/find_annotations',method=['OPTIONS','POST'])
@json_wrapper
@enable_cors
def find_annotations_handler():
    metadata_filters = json.load(request.body)
    print metadata_filters
    results = generic_find( find_annotations, metadata_filters)
    print "Results:", results
    return results

@route('/find_utterances',method=['OPTIONS','POST'])
@json_wrapper
@enable_cors
def find_utterances_handler():
    metadata_filters = json.load(request.body)
    print metadata_filters
    results = generic_find( find_utterances, metadata_filters)
    print "Results:", results
    return results

@route('/find_audio_events',method=['OPTIONS','POST'])
@json_wrapper
@enable_cors
def find_audio_events_handler():
    metadata_filters = json.load(request.body)
    print metadata_filters
    results = generic_find( find_audio_events, metadata_filters)
    print "Results:", results
    return results

@route('/find_pseudoterms',method=['OPTIONS','POST'])
@json_wrapper
@enable_cors
def find_pseudoterms_handler():
    metadata_filters = json.load(request.body)
    print metadata_filters
    results = generic_find( find_pseudoterms, metadata_filters)
    print "Results:", results
    return results



parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", default=12321)
args = parser.parse_args()

"""Now actually start the webserver"""
run(host='0.0.0.0', port=args.port, debug=True)
