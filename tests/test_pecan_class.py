import sys
sys.path.append('../')
#print sys.path
from disaggregator import PecanStreetDatasetAdapter as pecan

user_name = 'stomkins'
pw='PASSWORD'
host = "db.wiki-energy.org"
port = "5432"
db = "postgres"
db_url = "postgresql"+"://"+user_name+":"+pw+"@"+host+":"+port+"/"+db

p = pecan(db_url)
tables= p.set_table_names('PecanStreet_SharedData')
ids = p.get_meta_table('\"PecanStreet_SharedData\"',str(tables[0]))
print ids
#test = p.get_dataframe('select * from information_schema.tables')
#print test.columns
#for i in test['table_schema']:
#    print i

