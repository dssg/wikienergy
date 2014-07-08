import sys
import os.path
sys.path.append(os.path.join(os.pardir,os.pardir))
import disaggregator as da
import disaggregator.PecanStreetDatasetAdapter as psda
import pickle

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

## For regenerating a list of car ids.
def get_car_ids(schema,table,common_ids):
    '''
    Get a list of ids which seem to have cars
    '''
    columns = psda.get_table_column_names(schema,table)
    ev_traces = psda.generate_traces_for_appliance_by_dataids(schema,
        table, 'car1', common_ids)
    car_ids = [dataid for dataid,trace in zip(common_ids,ev_traces)\
        if trace.get_total_usage() > 0]
    return car_ids

# car_ids = get_car_ids(schema,tables[0],common_ids)
car_ids = [ 9729, 8197, 4641, 4135, 2638,
            9830, 624, 3192, 3723, 4767,
            7850, 1714, 6836, 7863, 7875,
            9932, 9934, 9937, 3795, 2769,
            5357, 1782, 9484, 2814, 7940,
            6941, 3367, 9609, 4957, 8046,
            661, 4998, 4505, 3482, 2470,
            4526, 5109, 8645, 1953, 8142,
            8669, 6910, 6139]

ev_traces = psda.generate_traces_for_appliance_by_dataids(schema,tables[2],
    'car1', car_ids)
with open('data/ev_traces_shared_03.pkl','w') as f:
    pickle.dump(ev_traces,f)

quit()

with open('data/ev_traces_shared_01.pkl', 'r') as f:
    ev_traces_shared_01 = pickle.load(f)

usages = [trace.get_total_usage() for trace in ev_traces_shared_01]

for usage in usages:
    print usage

import pdb;pdb.set_trace()
