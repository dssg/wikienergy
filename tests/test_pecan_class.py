import sys
sys.path.append('../')
#print sys.path
from disaggregator import PecanStreetDatasetAdapter as pecan

db_url = "postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres"

p = pecan(db_url)
tables = p.get_table_names('shared')
print tables

i,a = p.get_table_metadata('shared',str(tables[0]))
#apps = p.get_meta_table('\"PecanStreet_SharedData\"',str(tables[0]))
#traces = p.get_month_traces('SharedData',tables[0])
#print a
trace = p.get_month_traces_wo_time_align('shared',str(tables[0]),i[0])
#p.get_app_traces('shared',str(tables[0]),'refrigerator1')
