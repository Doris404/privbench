import dpspn.table.table as table
import dpspn.spn.spn as spn

import os
import json
import datetime
import argparse
from datetime import timezone, timedelta

parser = argparse.ArgumentParser()
parser.add_argument("--database", type=str, default="database", help="Name of database")
parser.add_argument("--spn_save", type=str, default="spn", help="spn save name")
parser.add_argument("--database_save", type=str, default="database_save", help="database save name")
args = parser.parse_args()

database = table.Table()
database.load(args.database)
print('Database loaded!')

spn = spn.Spn()
spn.gen_spn(database)
print('Spn generated!')
spn.save_spn(args.spn_save)
print('Spn saved!')

gen_database = spn.gen_database()
print('Database generated!')
gen_database.save(args.database_save)
print('Database saved!')