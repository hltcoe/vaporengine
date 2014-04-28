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


def now_to_millis():
    """Converts the current timestamp to millis since epoch"""
    return mktime(datetime.now().timetuple()) * 1000
