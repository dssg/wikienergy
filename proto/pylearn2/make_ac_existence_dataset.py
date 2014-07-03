import sys
sys.path.append('.')

import disaggregator as da
from pandas.tseries.offsets import DateOffset

db_url = "postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres"                                                                                         
ps_adapter = da.PecanStreetDatasetAdapter(db_url)

dataids = ps_adapter.get_unique_dataids("curated",2013,1,group=1)
traces = ps_adapter.get_month_traces("curated",2013,1,dataids[-1],group=1)

shift = traces[0].series.size
print shift
traces[1].series.index = traces[1].series.index + DateOffset(months=1,days=1)
print traces[0].series
print traces[0].series.index[-1] - traces[0].series.index[0] + traces[0].series.index
print traces[1].series
#print [float(t.get_total_usage()) for t in traces]
