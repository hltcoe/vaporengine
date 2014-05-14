# Python standard library modules
import argparse
import datetime as dt
import os
import tempfile

# Third party modules
from bottle import HTTPResponse, route, run, request, response, static_file, template
from bson import ObjectId
import bson.json_util
import pysox
try:
    import ujson as json
except:
    import json

# Local modules
from lib.database import init_dbconn
from vaporgasp.queries import (find_annotations, find_utterances,
                               find_pseudoterms, find_audio_events,
                               update_pseudoterm)
# TODO: Don't hard-code database settings to 'buckeye'
from settings import buckeye as settings
    
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

        # bson.json_util.dumps() knows how to convert Mongo ObjectId's to JSON
        return bson.json_util.dumps(resp)
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


"""Template testing"""
@route('/template_test')
def widget_handler():
    page = "<HTML><BODY>This {{fill}} should be filled in"
    return template(page,fill="**")


def generic_find(find_function, metadata_filters):
    """Does all the requisite conversions for pulling from the database
    and preparing to serve to the website.
    `find_function` should be one of the function from queries.py"""
    print metadata_filters
    dataset = metadata_filters['dataset'] #This maps to MongoDB table name
    print "from dataset:", dataset
    del metadata_filters['dataset']

    #SECURITY add whitelist of dataset names permitted
    db = init_dbconn(name = dataset, host=settings['DB_HOST'])

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
        #stringify mongoIDs (bson ids) before we pass it on
        result['_id'] = str(result['_id'])
        for bson_id_type in ['pt_id','utterance_id']:
            if bson_id_type in result:
                result[bson_id_type] = str(result[bson_id_type])
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
    print "Results*:", results
    return results


@route('/update_pseudoterm',method=['OPTIONS','POST'])
@json_wrapper
@enable_cors
def update_pseudoterm_header():
    update = json.load(request.body)
    _id = update['_id']
    del update['_id']

    dataset = update['dataset']
    del update['dataset']
    
    db = init_dbconn(name = dataset, host=settings['DB_HOST'])
    res = update_pseudoterm(db, _id, **update)
    
    return res

#Get Venncloud data for a single list of utterances
from vaporviz.vapor_venncloud import make_wc_datastructure
@route('/cloud_data_from_utterances',method=['OPTIONS','POST'])
@json_wrapper
@enable_cors
def cloud_data_handler():
    request_data = json.load(request.body) # Should have a 'dataset' and an 'utterances' field
    dataset = request_data['dataset']

    utterances = request_data['utterances']
    
    db = init_dbconn(name = dataset, host=settings['DB_HOST'])
    print request_data
    token_vector = make_wc_datastructure( db, utterances )

    print "Token Vector:", token_vector[:3]
    return token_vector



@route('/')
def index_page():
    vaporviz_path = os.path.dirname(os.path.realpath(__file__))
    return static_file('index.html', root=os.path.join(vaporviz_path, 'page_source'))


@route('/static/<filepath:path>')
def static_files(filepath):
    vaporviz_path = os.path.dirname(os.path.realpath(__file__))
    return static_file(filepath, root=os.path.join(vaporviz_path, 'static'))


@route('/audio/WAV/<filepath:path>')
def audio_static_wav(filepath):
    return static_file(filepath, root=settings['WAV_PATH'], mimetype='audio/wav')


@route('/audio/audio_event/<audio_event_id>.wav')
def audio_for_audio_event(audio_event_id):
    """
    """
    db = init_dbconn(name=settings['DB_NAME'], host=settings['DB_HOST'])
    audio_event = find_audio_events(db, _id=ObjectId(audio_event_id))[0]

    # Create a temporary directory
    tmp_directory = tempfile.mkdtemp()
    tmp_filename = os.path.join(tmp_directory, 'combined_clips.wav')

    # The first argument to CSoxStream must be a filename with a '.wav' extension.
    #
    # If the output file does not have a '.wav' extension, pysox will raise
    # an "IOError: No such file" exception.
    outfile = pysox.CSoxStream(
        tmp_filename,
        'w',
        settings['SOX_SIGNAL_INFO'])

    START_OFFSET = bytes("%f" % (audio_event['start_offset'] / 100.0))
    DURATION = bytes("%f" % (audio_event['duration'] / 100.0))

    utterance = find_utterances(db, _id=audio_event['utterance_id'])[0]
    input_filename = utterance['hltcoe_audio_path']

    infile = pysox.CSoxStream(input_filename)
    chain = pysox.CEffectsChain(infile, outfile)
    chain.add_effect(pysox.CEffect('trim', [START_OFFSET, DURATION]))
    chain.flow_effects()
    infile.close()

    outfile.close()

    # Read in audio data from temporary file
    wav_data = open(tmp_filename, 'rb').read()

    # Clean up temporary files
    os.remove(tmp_filename)
    os.rmdir(tmp_directory)

    return bytestring_as_file_with_mimetype(wav_data, 'audio/wav')


@route('/audio/pseudoterm/<pseudoterm_id>_audio_events.json')
@json_wrapper
def audio_events_for_pseudoterm(pseudoterm_id):
    """
    Returns a JSON object with information about the audio events
    associated with a pseudoterm
    """
    db = init_dbconn(name=settings['DB_NAME'], host=settings['DB_HOST'])
    pseudoterm = find_pseudoterms(db, _id=ObjectId(pseudoterm_id))[0]
    audio_events = find_audio_events(db, pt_id=pseudoterm['_id'])

    return audio_events[:10]


@route('/audio/pseudoterm/<pseudoterm_id>.wav')
def audio_for_pseudoterm(pseudoterm_id):
    """
    Creates a WAV file from multiple audio samples of a single pseudoterm
    """
    db = init_dbconn(name=settings['DB_NAME'], host=settings['DB_HOST'])
    pseudoterm = find_pseudoterms(db, _id=ObjectId(pseudoterm_id))[0]
    audio_events = find_audio_events(db, pt_id=pseudoterm['_id'])

    # Create a temporary directory
    tmp_directory = tempfile.mkdtemp()
    tmp_filename = os.path.join(tmp_directory, 'combined_clips.wav')

    # The first argument to CSoxStream must be a filename with a '.wav' extension.
    #
    # If the output file does not have a '.wav' extension, pysox will raise
    # an "IOError: No such file" exception.
    outfile = pysox.CSoxStream(
        tmp_filename,
        'w',
        settings['SOX_SIGNAL_INFO'])

    # TODO: Allow number of audio events to be specified as parameter, instead
    #       of hard-coded to 10
    for audio_event in audio_events[:10]:
        START_OFFSET = bytes("%f" % (audio_event['start_offset'] / 100.0))
        DURATION = bytes("%f" % (audio_event['duration'] / 100.0))

        utterance = find_utterances(db, _id=audio_event['utterance_id'])[0]
        input_filename = utterance['hltcoe_audio_path']

        infile = pysox.CSoxStream(input_filename)
        chain = pysox.CEffectsChain(infile, outfile)
        chain.add_effect(pysox.CEffect('trim', [START_OFFSET, DURATION]))
        chain.flow_effects()
        infile.close()

    outfile.close()

    # Read in audio data from temporary file
    wav_data = open(tmp_filename, 'rb').read()

    # Clean up temporary files
    os.remove(tmp_filename)
    os.rmdir(tmp_directory)

    return bytestring_as_file_with_mimetype(wav_data, 'audio/wav')


@route('/audio/pseudoterm/context/<pseudoterm_id>.wav')
def audio_for_pseudoterm_with_context(pseudoterm_id):
    """
    Creates a WAV file from multiple audio samples of a single pseudoterm
    """
    # TODO: Get seconds of context from HTTP parameter
    SECONDS_OF_CONTEXT = 0.5

    db = init_dbconn(name=settings['DB_NAME'], host=settings['DB_HOST'])
    pseudoterm = find_pseudoterms(db, _id=ObjectId(pseudoterm_id))[0]
    audio_events = find_audio_events(db, pt_id=pseudoterm['_id'])

    # Create a temporary directory
    tmp_directory = tempfile.mkdtemp()
    tmp_filename = os.path.join(tmp_directory, 'combined_clips.wav')

    # The first argument to CSoxStream must be a filename with a '.wav' extension.
    #
    # If the output file does not have a '.wav' extension, pysox will raise
    # an "IOError: No such file" exception.
    outfile = pysox.CSoxStream(
        tmp_filename,
        'w',
        settings['SOX_SIGNAL_INFO'])

    # TODO: Allow number of audio events to be specified as parameter, instead
    #       of hard-coded to 10
    for audio_event in audio_events[:10]:
        initial_start_offset = audio_event['start_offset'] / 100.0
        initial_duration = audio_event['duration'] / 100.0

        if initial_start_offset < SECONDS_OF_CONTEXT:
            start_offset = 0.0
            prefix_duration = initial_start_offset
        else:
            start_offset = initial_start_offset - SECONDS_OF_CONTEXT
            prefix_duration = SECONDS_OF_CONTEXT

        # TODO: Handle case where audio file is too short for requested context length
        suffix_duration = SECONDS_OF_CONTEXT

        duration = prefix_duration + initial_duration + suffix_duration

        print "INITIAL DURATION: %f" % initial_duration
        print "DURATION: %f" % duration

        utterance = find_utterances(db, _id=audio_event['utterance_id'])[0]
        input_filename = utterance['hltcoe_audio_path']

        start_offset = bytes("%f" % start_offset)
        duration = bytes("%f" % duration)

        infile = pysox.CSoxStream(input_filename)
        chain = pysox.CEffectsChain(infile, outfile)
        chain.add_effect(pysox.CEffect('trim', [start_offset, duration]))
        chain.flow_effects()
        infile.close()

    outfile.close()

    # Read in audio data from temporary file
    wav_data = open(tmp_filename, 'rb').read()

    # Clean up temporary files
    os.remove(tmp_filename)
    os.rmdir(tmp_directory)

    return bytestring_as_file_with_mimetype(wav_data, 'audio/wav')


@route('/audio/utterance/<utterance_id>.wav')
def audio_for_utterance(utterance_id):
    db = init_dbconn(name=settings['DB_NAME'], host=settings['DB_HOST'])

    utterance = find_utterances(db, _id=ObjectId(utterance_id))[0]
    utterance_filename = utterance['hltcoe_audio_path']

    return static_file(utterance_filename, root="/", mimetype='audio/wav')


def bytestring_as_file_with_mimetype(bytestring, mimetype):
    """
    Based on static_file() in bottle.py
    """
    headers = dict()
    headers['Content-Length'] = len(bytestring)
    headers['Content-Type'] = mimetype
    return HTTPResponse(bytestring, **headers)



parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", default=12321)
args = parser.parse_args()

"""Now actually start the webserver"""
run(host='0.0.0.0', port=args.port, debug=True)
