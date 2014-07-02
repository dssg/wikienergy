import sys
sys.path.append('.')

import disaggregator as da

db_url = "postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres"                                                                                         
ps_adapter = da.PecanStreetDatasetAdapter(db_url)

dataids = ps_adapter.get_unique_dataids("curated",1,2013,group=1)
traces = ps_adapter.get_month_traces("curated",2013,1,dataids[-1],group=1)

print traces[0].series
