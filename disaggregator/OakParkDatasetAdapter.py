"""
    .. module:: OakParkDatasetAdapter
    :platform: Unix
    :synopsis: Contains methods for importing data from Oak Park
    dataset.

    .. moduleauthor:: Phil Ngo <ngo.phil@gmail.com>
    .. moduleauthor:: Miguel Perez <miguel@invalid.com>
    .. moduleauthor:: Stephen Suffian <steve@invalid.com>
    .. moduleauthor:: Sabina Tomkins <sabina.tomkins@gmail.com>

"""


from appliance import ApplianceTrace
from appliance import ApplianceInstance
from appliance import ApplianceSet
from appliance import ApplianceType
import utils
import pymongo
import pandas as pd

def get_db_connection():
    connection = pymongo.MongoClient('ds059938.mongolab.com',59938)
    db = connection['oakparkhistoric']
    db.authenticate('anonymouseenergy', 'KaTard3i3')
    return db

def get_homes(db):
    """
    Returns a dictionary where each key is a home id and each value is a home.
    A home as meta_data, and a list of dates and power values in kwH.
    """
    houses =[]
    ids=[]
    c = db.usage.find()
    for co in c:
        ids.append(str(co['meta']['dataid']))
        houses.append(co)
    return {i:h for i,h in zip (ids,houses)}


def generate_trace_by_dataid(homes,dataid):
    '''
    Returns a trace.
    '''
    house = homes[dataid]
    dates = [x[0] for x in house['interval_readings']]
    values = [x[1]['value'] for x in house['interval_readings']]
    
    return ApplianceTrace(pd.Series(values, index = dates),house['meta'])

def resample_trace_by_month(trace,month):
    '''
    Returns a set of houses for a given month.
    '''
    return utils.resample_trace(trace,'MS')

def get_list_of_homes_with_certain_month_year(homes,year,month):
    '''
        Returns a list of homes which have complete trace info for given year and month.
        Assumes that homes is dict where keys are dataids and values are traces.
        '''
    complete_homes = []
    for h in homes.keys():
        dt_start = datetime(year,month,1)
        dt_end = datetime(year,month,calendar.monthrange(year,month)[1])
        index_start = homes[h].series.index.searchsorted(dt_start)
        index_end = homes[h].series.index.searchsorted(dt_end)
        if index_end-index_start==((dt_end-dt_start)*48).days:
            complete_homes.append(h)
    return complete_homes

def get_home_series_by_year_month(year,month,trace):
    '''
        Returns the home's series sliced by year and month.
        '''
    dt_start = datetime(year,month,1)
    dt_end = datetime(year,month,calendar.monthrange(year,month)[1])
    index_start = trace.series.index.searchsorted(dt_start)
    index_end = trace.series.index.searchsorted(dt_end)
    
    if index_start == 0 or index_end==0:
        return -1
    else:
        return  trace.series[index_start:index_end]


