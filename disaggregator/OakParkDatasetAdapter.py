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
from datetime import datetime
import calendar
import copy

source = "OakPark"

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

def homes_to_traces(homes):
    '''
       Returns a dictionary where the key is a home id and the value is an
       Appliance Trace.
    '''
    homes_new = {}
    for di in homes.keys():
        homes_new[di]=generate_trace_by_dataid(homes,di)
    return homes_new

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

def check_complete(home,year,month):
    year = int(year)
    month = int(month)
    dt_start = datetime(year,month,1)
    dt_end = datetime(year,month,calendar.monthrange(year,month)[1])
    index_start = home.series.index.searchsorted(dt_start)
    index_end = home.series.index.searchsorted(dt_end)
    return index_end-index_start==((dt_end-dt_start)*48).days

def get_home_series_by_year_month(home,year,month):
    '''
        Returns the home's series sliced by year and month.
        '''
    if check_complete(home,year,month):
        index_start = home.series.index.searchsorted(datetime(year,month,1))
        index_end = home.series.index.searchsorted(datetime(year,month,calendar.monthrange(year,month)[1]))
        return  home.series[index_start:index_end]

def get_list_of_homes_with_certain_year_month(homes,year,month):
    '''
        Returns a list of homes which have complete trace info for given year and month.
        Assumes that homes is dict where keys are dataids and values are traces.
        '''
    complete_homes = []
    for h in homes.keys():
        if check_complete(homes[h],year,month):
            complete_homes.append(h)
    return complete_homes

def generate_set_by_year_month(year,month):
    '''
        Returns an appliance set by month and year. Where there is one
        '''
    db = get_db_connection()
    homes = get_homes(db)
    homes_traces = homes_to_traces(homes)
    complete_homes = get_list_of_homes_with_certain_year_month(homes_traces,year,month)
    correct_homes = {}
    for h in complete_homes:
        correct_homes[h]=homes_traces[h]
        correct_homes[h].series=get_home_series_by_year_month(correct_homes[h],year,month)
        
        # print len(homes_traces[h].series)
        #print homes_traces[h].series.index[0]
    instances = [ApplianceInstance([t],t.metadata) for t in correct_homes]
    metadata_set= {'source':source,'dataids':complete_homes}
    return ApplianceSet(instances,metadata_set)

def generate_set_by_year_month(homes,year,month):
    '''
        Returns an appliance set by month and year. Where there is one
        '''
    # db = get_db_connection()
 
    homes_traces = homes_to_traces(copy.deepcopy(homes))
    complete_homes = get_list_of_homes_with_certain_year_month(homes_traces,year,month)
    correct_homes = {}
    for h in complete_homes:
        correct_homes[h]=homes_traces[h]
        correct_homes[h].series=get_home_series_by_year_month(homes_traces[h],year,month)
    
    # print len(homes_traces[h].series)
    #print homes_traces[h].series.index[0]
    instances = [ApplianceInstance([t],t.metadata) for t in correct_homes.values()]
    metadata_set= {'source':source,'dataids':complete_homes}
    return ApplianceSet(instances,metadata_set)

