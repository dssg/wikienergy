import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.pardir,os.pardir)))
import disaggregator as da
import disaggregator.PecanStreetDatasetAdapter as psda
import pickle


db_url = "postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres"
psda.set_url(db_url)

schema = 'shared'
table = 'validated_01_2014'
dataid = 3893
sample_rate = '15T'
appliance_set = psda.generate_set_by_table_and_dataid(
        schema, table, dataid, sample_rate)


appliance_set = appliance_set.generate_non_zero_set()

with open(os.path.join(os.pardir,os.pardir,'data','home_3893_set_01_2014.pkl'),'w') as f:
    pickle.dump(appliance_set,f)

