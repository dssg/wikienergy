"""
.. module:: PecanStreetDatasetAdapter
   :platform: Unix
   :synopsis: Contains methods for importing data from the pecan street
     dataset.

.. moduleauthor:: Phil Ngo <ngo.phil@gmail.com>
.. moduleauthor:: Miguel Perez <miguel.a.perez4@gmail.com>
.. moduleauthor:: Stephen Suffian <stephen.suffian@gmail.com>
.. moduleauthor:: Sabina Tomkins <sabina.tomkins@gmail.com>


"""

from appliance import ApplianceTrace
from appliance import ApplianceInstance
from appliance import ApplianceSet
from appliance import ApplianceType
import utils

import sqlalchemy
import pandas as pd
import numpy as np
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

def clean_dataframe(df,schema,drop_cols):
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
    utils.create_datetimeindex(df)

    # drop unnecessary columns
    df = df.drop(['dataid'], axis=1)
    if schema == 'curated':
        df = df.drop(['id'], axis=1)
    if len(drop_cols)!=0:
        df= df.drop(drop_cols,axis=1)

    return df


def generate_traces_by_table_and_dataid(schema,table,dataid,sample_rate=None):
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
            trace = ApplianceTrace(s,meta)
            if sample_rate:
                trace = trace.resample(sample_rate)
            traces.append(ApplianceTrace(s,meta))
    return traces

def generate_set_by_table_and_dataid(schema,table,dataid,sample_rate=None):
    '''
    Returns an ApplianceSet for given month and house.
    '''
    traces = generate_traces_by_table_and_dataid(schema,table,dataid,sample_rate)
    instances = [ApplianceInstance([t],t.metadata) for t in traces]
    metadata_set= {'source':source,
                'schema':schema,
                'table':table ,
                'dataid':instances[0].metadata['dataid']
                }
    return ApplianceSet(instances,metadata_set)

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
    table = get_table_name(schema, year, month, group, rate)
    return get_month_traces_from_table_name(schema, table, dataid)


def generate_appliance_trace(schema, table, appliance, dataid,
                             sample_rate=None, verbose=True):
    '''
    Return an appliance trace by dataid. The trace is in decimal form and in
    average kiloWatts.
    '''
    global schema_names, source
    schema_name = schema_names[schema]
    query= 'select {0},{1} from "{2}".{3} where dataid={4}'\
        .format(appliance,time_columns[schema],schema_name,table,dataid)
    print query
    df = get_dataframe(query)
    df = df.rename(columns={time_columns[schema]: 'time'})
    utils.create_datetimeindex(df)
    series = pd.Series(df[appliance],name = appliance).fillna(0)
    metadata = {'source':source,
            'schema':schema,
            'table':table ,
            'dataid':dataid,
            'device_name':series.name,
            }
    trace = ApplianceTrace(series,metadata)
    if sample_rate:
        trace = trace.resample(sample_rate)
    return trace

def generate_appliances_traces(
        schema,table,appliances,dataid,sample_rate=None,verbose=True):
    '''
    Return a list of appliance traces by dataid. Each trace is in decimal form
    and in average Watts.
    '''
    global schema_names, source
    schema_name = schema_names[schema]
    query= 'select {0},{1} from "{2}".{3} where dataid={4}'.format(
        ','.join(appliances), time_columns[schema], schema_name, table, dataid)
    if verbose:
        print query
    df = get_dataframe(query)
    df = df.rename(columns={time_columns[schema]: 'time'})
    utils.create_datetimeindex(df)
    traces = []
    for appliance in appliances:
        series = pd.Series(df[appliance],name = appliance).fillna(0)
        metadata = {'source':source,
                    'schema':schema,
                    'table':table ,
                    'dataid':dataid,
                    'device_name':series.name,
                    }
        trace = ApplianceTrace(series,metadata)
        if sample_rate:
            trace = trace.resample(sample_rate)
        traces.append(trace)
    return traces

def generate_appliance_instance(
        schema,tables,appliances,dataid,sample_rate=None,verbose=True):
    """
    Return an appliance instance from consecutive tables. Concatenates traces.
    """
    traces = [generate_appliance_trace(schema,table,appliances,dataid,
                  sample_rate,verbose) for table in tables]
    traces = [utils.concatenate_traces(traces)]
    return ApplianceInstance(traces,traces[0].metadata)

def generate_appliances_instances(
        schema,tables,appliances,dataid,sample_rate=None,verbose=True):
    """
    Return an appliance instances from consecutive tables. Concatenates traces.
    """
    all_traces = [generate_appliances_traces(schema,table,appliances,dataid,
                      sample_rate,verbose) for table in tables]

    # transpose
    appliance_traces = list(zip(*all_traces))

    # concatenate by appliance
    appliance_traces = [utils.concatenate_traces(traces)
                        for traces in appliance_traces]
    return [ApplianceInstance([trace],trace.metadata)
            for trace in appliance_traces]

def generate_instances_for_appliance_by_dataids(
        schema, tables, appliance, dataids, sample_rate=None):
    """
    Returns instances for a single appliance type across a set of dataids
    """
    instances = [generate_appliance_instance(schema, tables, appliance, dataid,
                 sample_rate) for dataid in dataids]
    return instances

def generate_traces_for_appliance_by_dataids(
        schema, table, appliance, ids, sample_rate=None):
    '''
    Returns traces for a single appliance type across a set of dataids.
    '''
    traces = [generate_appliance_trace(schema,table,appliance,id_,sample_rate)\
              for id_ in ids]
    return traces

def generate_traces_for_appliances_by_dataid(
        schema, table, appliances, dataid, sample_rate=None):
    '''
    Returns traces for a list of appliance types across a set of dataids.
    Wrapper for `generate_appliances_traces` function
    '''
    traces = generate_appliances_traces(schema, table, appliances, dataid,
                                        sample_rate)
    return traces

def generate_instances_for_appliances_by_dataids(
        schema, tables, appliances, dataids, sample_rate=None):
    """
    Returns instances for a list of appliances across a set of dataids
    """
    #TODO probably a more efficient way to do this
    instances = [generate_appliances_instances(schema, tables, appliances,
                 dataid, sample_rate) for dataid in dataids]
    return instances


def generate_traces_for_appliances_by_dataids(
        schema, table, appliances, dataids, sample_rate=None):
    '''
    Returns a list of lists of traces for appliance types for a list of dataids.
    Ex. `traces[0][3]` gets the fourth appliance trace for the first dataid.
    '''
    traces = [generate_traces_for_appliances_by_dataid(
                  schema, table, appliances, dataid, sample_rate)
              for dataid in dataids]
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
            'table':table,
            'device_name':trace.series.name,
            'dataid':trace.metadata['dataid'],
            }
        instances.append(ApplianceInstance([trace],metadata_instance))
    return ApplianceType(instances,metadata_type)

def get_dataframe(query):
    '''
    Returns a Pandas dataframe with the query results
    '''
    global eng
    eng_object = eng.execute(query)
    #import pdb;pdb.set_trace()
    df = pd.DataFrame.from_records(eng_object.fetchall())
    df.columns = eng_object.keys()
    return df

def get_use_for_active_windows(schema, tables, appliances, dataids,
                               window_length, window_stride,
                               drop_percentile=10, sample_rate='15T'):
    '''Given a list of consecutive tables, returns windows of total use data
    for which the appliance waas active.

    Appliances should not include the 'use' column. Drops the lowest
    drop_percentile samples. Use appliances=None for unfiltered windows.
    '''
    if appliances:
        query_appliances = appliances[:]
    else:
        query_appliances = []
    query_appliances.append('use')
    instances = generate_instances_for_appliances_by_dataids(
            schema,tables,query_appliances,dataids,sample_rate)
    usages = [instances_for_id[-1] for instances_for_id in instances]
    instances = [instances_for_id[:-1] for instances_for_id in instances]
    all_appliance_windows = []
    for usage, instances_ in zip(usages,instances): # iterate over dataids
        assert(len(usage.traces) == 1)
        usage_windows = utils.get_trace_windows(usage.traces[0],window_length,
                window_stride)
        appliance_windows = []
        if not appliances:
            if drop_percentile is not 0:
                print "Warning: ignoring drop_percentile"

            # remove nans
            windows = np.nan_to_num(np.array(usage_windows))
            appliance_windows.append(windows)
        else:
            for instance in instances_: # iterate over appliances
                assert(len(instance.traces) == 1)
                appliance_window_array = utils.get_trace_windows(
                        instance.traces[0],window_length,window_stride)
                window_totals = np.sum(appliance_window_array,axis = 1)
                # drop usage windows for which the appliance totals are in the
                # bottom few percentiles
                n_keep = window_totals.shape[0]*(100-drop_percentile)/100
                keep_indices = sorted(np.argsort(window_totals)[::-1][:n_keep])
                # remove nans
                windows = np.array([usage_windows[i] for i in keep_indices])
                windows = np.nan_to_num(windows)
                appliance_windows.append(windows)
        all_appliance_windows.append(appliance_windows)
    return all_appliance_windows

def get_appliance_detection_arrays(schema,tables,appliance,window_length,
                                   window_stride,drop_percentile,verbose=True):
    """Given an appliance, get all information from a schema in the database
    about what usage looks like when the appliance is present.
    """
    if verbose:
        print "Fetching dataids"
    all_ids = utils.get_common_ids(
            [get_dataids_with_real_values(schema,table,'use')
                for table in tables])
    appliance_ids = utils.get_common_ids(
            [get_dataids_with_real_values(schema,table,appliance)
                for table in tables])
    no_appliance_ids = sorted(list(set(all_ids) - set(appliance_ids)))

    # generate random dataid indices
    app_i_train, app_i_valid, app_i_test = \
        utils.get_train_valid_test_indices(len(appliance_ids))
    no_app_i_train, no_app_i_valid, no_app_i_test = \
        utils.get_train_valid_test_indices(len(no_appliance_ids))

    set_indices = [("Training",app_i_train,no_app_i_train),
                   ("Validation",app_i_valid,no_app_i_valid),
                   ("Testing",app_i_test,no_app_i_test)]

    training_sets = []

    for set_name,app_i,no_app_i in set_indices:
        if verbose:
            print set_name
        # get dataids
        appliance_ids_ = [appliance_ids[i] for i in app_i]
        no_appliance_ids_ = [no_appliance_ids[i] for i in no_app_i]

        # get windows for each dataid
        if verbose:
            print "Fetching samples for key = 1"
        active_appliance_windows = get_use_for_active_windows(
                schema,tables,[appliance],appliance_ids_,
                window_length,window_stride,drop_percentile)
        if verbose:
            print "Fetching samples for key = 0"
        other_windows = get_use_for_active_windows(
                schema,tables,None,no_appliance_ids_,
                window_length,window_stride,drop_percentile=0)

        # concatenate results for different dataids
	try:
            all_appliance_windows = np.concatenate(
                    [windows[0] for windows in active_appliance_windows],axis=0)
            all_other_windows = np.concatenate(
                    [windows[0] for windows in other_windows],axis=0)
        except IndexError:
            import pdb; pdb.set_trace()
        # make one-hot answer-key arrays
        appliance_keys = np.array([[0,1] for _ in all_appliance_windows])
        no_appliance_keys = np.array([[1,0] for _ in all_other_windows])

        # concatenate all training examples
        X = np.concatenate([all_appliance_windows,all_other_windows],axis=0)
        y = np.concatenate([appliance_keys,no_appliance_keys],axis=0)

        training_sets.append((X,y))
    train, valid, test = training_sets
    return train, valid, test

class SchemaError(Exception):
    '''Exception raised for errors in the schema.

        Attributes:
            schema  -- nonexistent schema
    '''
    def __init__(schema):
        self.schema = schema

    def __str__(self):
        return "Schema {} not supported or nonexistent.".format(self.schema)
