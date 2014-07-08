import sys
import os.path
sys.path.append(os.path.join(os.pardir,os.pardir))
import disaggregator as da
import disaggregator.PecanStreetDatasetAdapter as psda

db_url = "postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres"
psda.set_url(db_url)

schema = 'shared'
tables = [u'validated_01_2014',
          u'validated_02_2014',
          u'validated_03_2014',
          u'validated_04_2014',
          u'validated_05_2014',]

all_ids = [psda.get_table_dataids(schema,table) for table in tables]
common_ids = da.get_common_ids(all_ids)
columns = psda.get_table_column_names(schema,tables[0])

if 'car1' not in columns:
    print "car not found"
    exit()
else:
    print "car found"

ev_traces = psda.generate_traces_for_appliance_by_dataids(schema, tables[0],
    'car1', common_ids)

for dataid,ev_trace in zip(common_ids,ev_traces):
    print "dataid: {}, ev total: {}".format(dataid,ev_trace.get_total_usage())

import pdb;pdb.set_trace()
