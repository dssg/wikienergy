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
    return pd.Series(values, index = dates)



