from appliance import ApplianceTrace
from appliance import ApplianceInstance
from appliance import ApplianceSet
from appliance import ApplianceType
import fhmm

import pandas as pd
import numpy as np

def generate_trace(start,periods,freq):
    """
    Returns a generated appliance trace for a particular time period.
    Ex) generate_trace(datetime.datetime(2013,1,1),96,'15T'))
    """
    rng = pd.date_range(start, periods=periods, freq=freq)
    series = pd.Series(np.random.randn(periods) + 1, index=rng)

    return ApplianceTrace(series,{"source": "generated"})

def generate_instance(starts,periods,freq):
    """
    Returns a generated appliance instance for a particular time period.
    """
    traces = []
    for start in starts:
        traces.append(generate_trace(start,periods,freq))
    return ApplianceInstance(traces,{"source": "generated"})
