import sys
import os.path
sys.path.append(os.path.join(os.pardir,os.pardir))

import disaggregator as da
import disaggregator.PecanStreetDatasetAdapter as psda

import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('appliance')
args = parser.parse_args()

db_url = "postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres"
psda.set_url(db_url)

schema = 'shared'
tables = [u'validated_01_2014',
          u'validated_02_2014',
          u'validated_03_2014',
          u'validated_04_2014',
          u'validated_05_2014',]

ids = []
for table in tables:
    ids.append(psda.get_dataids_with_real_values(schema,table,args.appliance))

print sorted(da.utils.get_common_ids(ids))
