#!/usr/bin/env python

import argparse
import codecs

from bson import ObjectId

from lib.database import init_dbconn
from lib.queries import find_pseudoterms, update_pseudoterm
from settings import settings

parser = argparse.ArgumentParser()
parser.add_argument("dataset_name")
parser.add_argument("backup_file")
args = parser.parse_args()

db = init_dbconn(name=settings[args.dataset_name]['DB_NAME'], host=settings[args.dataset_name]['DB_HOST'])

backup_file = codecs.open(args.backup_file, "r", encoding="utf-8")

for line in backup_file.readlines():
    zr_pt_id, annotation = line.strip().split('\t')
    zr_pt_id = int(zr_pt_id)
    try:
        pseudoterm = find_pseudoterms(db, zr_pt_id=zr_pt_id)[0]
        update = {'annotated': True, 'eng_display': annotation}
        update_pseudoterm(db, pseudoterm['_id'], **update)
    except IndexError:
        print "Unable to find Pseudoterm with ID '%s'" % zr_pt_id

backup_file.close()
