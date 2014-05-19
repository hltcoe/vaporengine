#!/usr/bin/env python

import argparse
import codecs

from bson import ObjectId

from lib.database import init_dbconn
from settings import settings
from vaporgasp.queries import find_pseudoterms, update_pseudoterm

parser = argparse.ArgumentParser()
parser.add_argument("backup_file")
args = parser.parse_args()

db = init_dbconn(name=settings['DB_NAME'], host=settings['DB_HOST'])

backup_file = codecs.open(args.backup_file, "r", encoding="utf-8")

for line in backup_file.readlines():
    pseudoterm_name, annotation = line.strip().split('\t')
    try:
        pseudoterm = find_pseudoterms(db, native_display=pseudoterm_name)[0]
        update = {'annotated': True, 'display_name': annotation}
        update_pseudoterm(db, pseudoterm['_id'], **update)
    except IndexError:
        print "Unable to find Pseudoterm with ID '%s'" % pseudoterm_name

backup_file.close()
