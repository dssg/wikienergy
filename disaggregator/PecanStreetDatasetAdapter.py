"""
.. module:: PecanStreetDatasetAdapter
   :platform: Unix
   :synopsis: Contains methods for importing data from the pecan street
     dataset.

.. moduleauthor:: Phil Ngo <ngo.phil@gmail.com>
.. moduleauthor:: Stephen Suffian <steve@invalid.com>
.. moduleauthor:: Sabina Tomkins <sabina.tomkins@gmail.com>

"""

from appliance import ApplianceTrace
from appliance import ApplianceInstance
from appliance import ApplianceSet
from appliance import ApplianceType
import utils

import sqlalchemy
import pandas as pd
import decimal

url = ''
source = "PecanStreet"
eng = None
schema_names =    {'curated': 'PecanStreet_CuratedSets',
                    'raw':     'PecanStreet_RawData',
                    'shared':  'PecanStreet_SharedData'}

time_columns =    {'curated': 'utc_15min',
                    'raw':     'localminute15minute',
                    'shared':  'localminute'}

invalid_columns = {'curated': ['id', 'utc_15min'],
                    'raw':     ['localminute15minute'],
                    'shared':  ['localminute']}

table_lookup = {'shared':
        {'2014':
            {'01':'validated_01_2014',
             '02':'validated_02_2014',
             '03':'validated_03_2014',
             '04':'validated_04_2014',
             '05':'validated_05_2014'
             }
        },
    'curated':
        {'1':
            {'2012':
                {'12': 'group1_disaggregated_2012_12'},
             '2013':
                {'01': 'group1_disaggregated_2013_01',
                 '02': 'group1_disaggregated_2013_02',
                 '03': 'group1_disaggregated_2013_03',
                 '04': 'group1_disaggregated_2013_04',
                 '05': 'group1_disaggregated_2013_05',
                 '06': 'group1_disaggregated_2013_06',
                 '07': 'group1_disaggregated_2013_07',
                 '08': 'group1_disaggregated_2013_08',
                 '09': 'group1_disaggregated_2013_09',
                 '10': 'group1_disaggregated_2013_10',
                 '11': 'group1_disaggregated_2013_11'}},
        '2':
            {'2012':
                {},
            '2013':
                {'01': 'group2_disaggregated_2013_01',
                '02': 'group2_disaggregated_2013_02',
                '03': 'group2_disaggregated_2013_03',
                '04': 'group2_disaggregated_2013_04',
                '05': 'group2_disaggregated_2013_05',
                '06': 'group2_disaggregated_2013_06',
                '07': 'group2_disaggregated_2013_07',
                '08': 'group2_disaggregated_2013_08',
                '09': 'group2_disaggregated_2013_09',
                '10': 'group2_disaggregated_2013_10',
                '11': 'group2_disaggregated_2013_11'}},
        '3':
            {'2012':
                {},
            '2013':
                {'05': 'group3_disaggregated_2013_05',
                '06': 'group3_disaggregated_2013_06',
                '07': 'group3_disaggregated_2013_07',
                '08': 'group3_disaggregated_2013_08',
                '09': 'group3_disaggregated_2013_09',
                '10': 'group3_disaggregated_2013_10',
                '11': 'group3_disaggregated_2013_11'} },
        'other':
            ['west_pv_fall_2013',
            'south_pv_fall_2013',
            'pv_summer_2013',
            'southwest_pv_fall_2013',
            'ev_fall_2013']},
    'raw':
        {'2014':
            {'1T':'egauge_minutes_2014',
            '15T':'egauge_15min_2014'},
        '2013':
            {'1T':'egauge_minutes_2013',
            '15T':'egauge_15min_2013'},
        '2012':
            {'1T':'egauge_minutes_2012',
            '15T':'egauge_15min_2012'}
        }
    }

def set_url(db_url):
    '''
    Initialize an adapter using a database url_string. Consider the following
    example: db_url="postgresql://user_name:password@host.url:port/db"
    '''
    global url
    global eng
    url = db_url
    eng = sqlalchemy.create_engine(url)

def get_table_names(schema):
    '''
    Returns a list of tables in the schema.
    '''
    global schema_names
    df = get_dataframe('select * from information_schema.tables')
    df = df.groupby(['table_schema','table_name'])
    groups = [group for group in df.groups]
    table_names = [t for (s,t) in groups if s == '{}'\
        .format(schema_names[schema])]
    return table_names

def verify_same_range(pair,pairs):
    '''
    Check that all data points have the same range
    '''
    #TODO this should go into utils
    pass

def get_table_dataids(schema,table):
    '''
    Returns a list of dataids for this schema and table
    '''
    id_query = 'select distinct dataid from "{}".{}'\
        .format(schema_names[schema],table)
    ids = [row[0] for row in eng.execute(id_query).fetchall()]
    return ids

def get_table_column_names(schema,table):
    '''
    Returns a list of column names for this schema and table
    '''
    col_query = "select column_name from information_schema.columns where\
        table_schema='{}' and table_name = '{}'"\
        .format(schema_names[schema],table)
    cols = [row[0] for row in eng.execute(col_query).fetchall()]
    return cols

def get_table_dataids_and_column_names(schema,table):
    '''
    Returns a list of dataids for this schema and table, and a list of the
    column names for this schema and table
    '''
    id_query = 'select distinct dataid from "{}".{}'\
        .format(schema_names[schema],table)
    col_query = "select column_name from information_schema.columns where\
        table_schema='{}' and table_name = '{}'"\
        .format(schema_names[schema],table)
    ids = [row[0] for row in eng.execute(id_query).fetchall()]
    cols = [row[0] for row in eng.execute(col_query).fetchall()]
    return ids, cols

def get_unique_dataids(schema,year,month,group=None):
    '''
    Returns a list of dataids for a specifc schema ("curated","shared", or
    "raw"), month (int), year (int), and [group (int) - only if "curated"].
    '''
    if schema == "curated":
        schema_name = self.schema_names[schema]
        query = 'select distinct dataid from "{0}"\
            .group{1}_disaggregated_{2}_{3:02d}'\
            .format(schema_name,group,year,month)
        df = self.get_dataframe(query)
        return list(df["dataid"])
    elif schema == "shared":
        raise NotImplementedError
    elif schema == "raw":
        raise NotImplementedError
    else:
        raise SchemaError(schema)

def time_align():
    '''
    Checks that for all traces in a home the total time lengths are the
    same
    '''
    # TODO this should go into utils
    pass

def clean_dataframe(df,schema,drop_cols):
    # TODO update this to use "curated" "shared" or "raw"
    #   instead of full frame name
    '''
    Cleans a dataframe queried directly from the database by renaming the db 
    time column (ex. UTC_15MIN) to a column name 'time'. It then converts the
    time column to datetime objects and reindexes the dataframe to the time
    column before dropping that column from the dataframe. It also drops any
    columns included in the list drop_cols. The columns 'id' and 'dataid' are 
    also dropped.
    '''
    # change the time column name
    global time_columns
    df = df.rename(columns={time_columns[schema]: 'time'})

    # use a DatetimeIndex
    df['time'] = pd.to_datetime(df['time'],utc=True)
    df.set_index('time', inplace=True)

    # drop unnecessary columns
    df = df.drop(['dataid'], axis=1)
    if schema == 'curated':
        df = df.drop(['id'], axis=1)
    if len(drop_cols)!=0:
        df= df.drop(drop_cols,axis=1)

    return df


def check_sample_rate(schema,sampling_rate):
    # TODO get from the data directly not like this
    accepted_rates = {'curated':'15T' ,'raw':'15' ,'shared':'1T' }

def generate_month_traces_from_table_name(schema,table,dataid):
    '''
    Returns a list of traces for one house and one month
    '''
    global schema_names,invalid_columns,source
    if schema not in ['curated','raw','shared']:
        raise SchemaError(schema)
    schema_name = schema_names[schema]
    query = 'select * from "{0}".{1} where dataid={2}'\
        .format(schema_name, table, dataid)
    # TODO NEED TO CHANGE IDS
    # TODO error checking that query worked
    df = get_dataframe(query).fillna(0)

    df= clean_dataframe(df, schema,[])
    traces = []
    for col in df.columns:
        if not col in invalid_columns[schema]:
            s = pd.Series(df[col],name = col)
            meta={'source':source,
                'schema':schema,
                'table':table ,
                'dataid':dataid,
                'device_name':s.name
                }
            traces.append(ApplianceTrace(s,meta))
    return traces

def generate_set_by_house_and_month(schema,table,dataid):
    '''
    Returns an ApplianceSet for given month and house.
    '''
    traces = get_month_traces_from_table_name(schema,table,dataid)
    instances = [ApplianceInstance(t.series,t.metadata) for t in traces]
    metadata = instance[0].metadata.pop("device_name")
    return ApplianceSet(instances,metadata)

def get_table_name(schema,year,month,group=None, rate = None):
    '''
    Given the year, month, and group return the table name.
    '''
    if schema=='curated':
        if group in table_lookup[schema]:
            if year in table_lookup[schema][group]:
                if month in table_lookup[schema][group][year]:
                    return table_lookup[schema][group][year][month]
        else:
            return
    elif schema=='shared':
        if year in table_lookup[schema]:
            if month in table_lookup[schema][year]:
                return table_lookup[schema][year][month]
        else:
            return
    elif schema=='raw':
        if year in table_lookup[schema]:
            if rate in table_lookup[schema][year]:
                return table_lookup[schema][year][rate]
        else:
            return
    else:
        raise SchemaError(schema)


def generate_month_traces_from_attributes(schema,year,month,group=None, rate = None, dataid=None):
    '''
    Returns a list of traces from a given month. It first finds the table
    name associated with that month.
    '''
    table = get_table_name(schema, year, month,group,rate)
    return get_month_traces_from_table_name(schema,table,dataid)


def generate_appliance_trace(schema,table,appliance,dataid,sample_rate=None):
    '''
    Return an appliance trace by dataid. The trace is in decimal form and in
    average Watts.
    '''
    global schema_names, source
    schema_name = schema_names[schema]
    query= 'select {0}, {1} from "{2}".{3} where dataid={4}'\
        .format(appliance,time_columns[schema],schema_name,table,dataid)
    print query
    df = get_dataframe(query)
    df = df.rename(columns={time_columns[schema]: 'time'})
    df['time'] = pd.to_datetime(df['time'],utc=True)
    df.set_index('time', inplace=True)
    series = pd.Series(df[appliance],name = appliance) * decimal.Decimal(1000.0)
    metadata = {'source':source,
            'schema':schema,
            'table':table ,
            'dataid':dataid,
            'device_name':series.name,
            }
    trace = ApplianceTrace(series,metadata)
    if sample_rate:
        trace = utils.resample_trace(trace,sample_rate)
    return trace

def generate_traces_for_appliance_by_dataids(
        schema, table, appliance, ids, sample_rate=None):
    '''
    Returns traces for a single appliance type across a set of dataids.
    '''
    traces = [generate_appliance_trace(schema,table,appliance,id_,sample_rate)\
              for id_ in ids]
    return traces

def get_dataids_with_real_values(schema,table,appliance):
    '''
    Returns ids that contain non-'NoneType' values for a given appliance
    '''
    global schema_names, source
    schema_name = schema_names[schema]
    query = """
        WITH summary AS (
            SELECT v.dataid,
                   v.{0},
                   ROW_NUMBER() OVER(PARTITION BY v.dataid) AS rk
            FROM "{1}".{2} v)
        SELECT s.dataid
        FROM summary s
        WHERE s.rk = 1 and s.{0} is not null
        """.format(appliance,schema_name,table)
    real_ids = [row[0] for row in eng.execute(query).fetchall()]
    return real_ids

def generate_type_for_appliance_by_dataids(schema,table,appliance,ids):
    '''
    Given an appliance and a list of dataids, generate an ApplianceType
    '''
    traces = generate_traces_for_appliance_by_dataids(schema,table,appliance,
            ids)
    instances=[]

    metadata_type = {'source':source,
                'schema':schema,
                'table':table ,
                'device_name':traces[0].series.name,
                }
    for trace in traces:
        metadata_instance = {'source':source,
            'schema':schema,
            'table':table ,
            'device_name':traces[0].series.name,
            'dataid':traces[0].metadata['dataid'],
            }
        instances.append(ApplianceInstance([trace],metadata_instance))
    return ApplianceType(instances,metadata_type)

def get_dataframe(query):
    '''
    Returns a Pandas dataframe with the query results
    '''
    global eng
    eng_object = eng.execute(query)
    df = pd.DataFrame.from_records(eng_object.fetchall())
    df.columns = eng_object.keys()
    return df

class SchemaError(Exception):
    '''Exception raised for errors in the schema.

        Attributes:
            schema  -- nonexistent schema
    '''
    def __init__(schema):
        self.schema = schema

    def __str__(self):
        return "Schema {} not supported or nonexistent.".format(self.schema)
