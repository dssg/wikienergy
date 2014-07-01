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

[i,a] = p.get_meta_table('\"PecanStreet_SharedData\"',str(tables[0]))
#apps = p.get_meta_table('\"PecanStreet_SharedData\"',str(tables[0]))
#traces = p.get_month_traces('SharedData',tables[0])
#print a
p.get_app_traces('\"PecanStreet_SharedData\"',str(tables[0]),'refrigerator1')

