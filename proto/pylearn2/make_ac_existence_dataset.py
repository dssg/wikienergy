import sys
sys.path.append('.')

import disaggregator as da
from pandas.tseries.offsets import DateOffset
import numpy as np

db_url = "postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres"
psda = da.PecanStreetDatasetAdapter(db_url)

dataids = psda.get_unique_dataids("curated",2013,1,group=1)
traces = psda.get_month_traces("curated",2013,1,dataids[-1],group=1)
instances = [da.ApplianceInstance([trace]) for trace in traces]
usage_order = np.argsort([i.traces[0].get_total_usage() for i in instances])[::-1]

top_5_instances = [instances[i] for i in usage_order[1:6]]

print [inst.traces[0].series.name for inst in top_5_instances]

print da.aggregate_traces(traces, {"name":"aggregated"}).series
