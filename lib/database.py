import pymongo

import sys
#print sys.path

from lib.timestamping import datestring_to_millis
from settings import buckeye
DB_HOST = buckeye['DB_HOST']
DB_NAME = buckeye['DB_NAME']
DB_PORT = buckeye['DB_PORT']


###
### Connect handling
###

def init_dbconn(host=DB_HOST, port=DB_PORT, name=DB_NAME):
    """Simply opens the connections or pulls a connection from PyMongo's
    built-in connection pooling.
    """
    dbc = pymongo.Connection(host=host, port=port)
    return dbc[name]


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
### Common Argument Handling
###

def gen_date_args(start_date, end_date):
    """Generates a dictionary representing a date range query. If the date
    arguments are strings, they are converted using `datestring_to_millis`.

    A dictionary representing the date query is returned.
    """
    if start_date and isinstance(start_date, (unicode, str)):
        start_date = datestring_to_millis(start_date)
    if end_date and isinstance(end_date, (unicode, str)):
        end_date = datestring_to_millis(end_date)
    
    # The date query looks like: {'date': {'$gt': start_date, '$lt': end_date}}
    date_args = {}
    if start_date:
        date_args['$gt'] = start_date
    if end_date:
        date_args['$lt'] = end_date

    return date_args
