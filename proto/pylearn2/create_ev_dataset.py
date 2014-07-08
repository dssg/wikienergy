import sys
import os.path
sys.path.append(os.path.join(os.pardir,os.pardir))
import disaggregator as da
import disaggregator.PecanStreetDatasetAdapter as psda

db_url = "postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres"
psda.set_url(db_url)
schema = 'shared'


table_names = psda.get_table_names(schema)

all_ids = []
all_columns = []
for table_name in table_names:
    ids,columns = psda.get_table_dataids_and_column_names(schema,table_name)
    all_ids.append(ids)
    all_columns.append(columns)

common_ids = da.get_common_ids(all_ids)
import pdb;pdb.set_trace()
