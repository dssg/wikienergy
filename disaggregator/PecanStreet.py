from appliance import ApplianceTrace
from appliance import ApplianceInstance
from appliance import ApplianceSet

import sqlalchemy
import pandas as pd

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

table_lookup= {'shared':{'2014':{'01':'validated_01_2014','02':'validated_02_2014','03':'validated_03_2014','04':'validated_04_2014','05':'validated_05_2014'}},'curated':{'1': {'2012': {'12': 'group1_disaggregated_2012_12'},'2013': {'01': 'group1_disaggregated_2013_01','02': 'group1_disaggregated_2013_02','03': 'group1_disaggregated_2013_03','04': 'group1_disaggregated_2013_04','05': 'group1_disaggregated_2013_05','06': 'group1_disaggregated_2013_06','07': 'group1_disaggregated_2013_07', '08': 'group1_disaggregated_2013_08', '09': 'group1_disaggregated_2013_09','10': 'group1_disaggregated_2013_10', '11': 'group1_disaggregated_2013_11'}},'2': {'2012': {}, '2013': {'01': 'group2_disaggregated_2013_01', '02': 'group2_disaggregated_2013_02', '03': 'group2_disaggregated_2013_03', '04': 'group2_disaggregated_2013_04', '05': 'group2_disaggregated_2013_05', '06': 'group2_disaggregated_2013_06', '07': 'group2_disaggregated_2013_07', '08': 'group2_disaggregated_2013_08', '09': 'group2_disaggregated_2013_09', '10': 'group2_disaggregated_2013_10', '11': 'group2_disaggregated_2013_11'}},'3': {'2012': {}, '2013': {'05': 'group3_disaggregated_2013_05', '06': 'group3_disaggregated_2013_06','07': 'group3_disaggregated_2013_07', '08': 'group3_disaggregated_2013_08', '09': 'group3_disaggregated_2013_09', '10': 'group3_disaggregated_2013_10','11': 'group3_disaggregated_2013_11'} }, 'other':['west_pv_fall_2013','south_pv_fall_2013','pv_summer_2013', 'southwest_pv_fall_2013','ev_fall_2013']},'raw': {'2014':{'1T':'egauge_minutes_2014','15T':'egauge_15min_2014'},'2013':{'1T':'egauge_minutes_2013','15T':'egauge_15min_2013'},'2012':{'1T':'egauge_minutes_2012','15T':'egauge_15min_2012'}} }

def set_url(db_url):
    global url
    global eng
    url = db_url
    '''Initialize an adapter using a database url_string.Consider the following example: db_url="postgresql://user_name:password@host.url:port/db"
    '''
    eng = sqlalchemy.create_engine(url)






    

def get_table_names(schema):
        '''
        Returns a list of tables in the schema.
        '''
        global schema_names
        df = get_dataframe('select * from information_schema.tables')
        df = df.groupby(['table_schema','table_name'])
        groups = [group for group in df.groups]
        # print groups
        #print self.schema_names[schema]
        table_names = [t for (s,t) in groups if s == '"{}"'.format(schema_names[schema])]
        return table_names

def verify_same_range(pair,pairs):
        '''
        Check that all data points have the same range
        '''
        pass

def get_table_metadata(schema,table):
        '''
        Returns a tuple where the first element is a list of data ids for this
        schema.table and the second element is a list of the appliances
        included in this schema.table
        '''
        q = 'select distinct dataid from "{}".{}'.format(schema_names[schema],table)
        result = eng.execute(q)
        ids = result.fetchall()
        q = 'select * from "{}".{} where dataid={}'.format(schema_names[schema],table,ids[0][0])
        result = eng.execute(q)
        apps = result.keys()
        ids= [a[0] for a in ids]
        apps = [str(a) for a in apps ]
        return ids, apps

def get_unique_dataids(schema,year,month,group=None):
        '''
        Returns a list of dataids for a specifc schema ("curated","shared", or
        "raw"), month (int), year (int), and [group (int) - only if "curated"].
        '''
        if schema == "curated":
            schema_name = self.schema_names[schema]
            query = 'select distinct dataid from "{0}".group{1}_disaggregated_{2}_{3:02d}'.format(schema_name,group,year,month)
            df = self.get_dataframe(query)
            return list(df["dataid"])
        elif schema == "shared":
            raise NotImplementedError
        elif schema == "raw":
            raise NotImplementedError
        else:
            raise SchemaError(schema)



def time_align():
        '''Checks that for all traces in a home the total time lengths are the same'''
        pass

def clean_dataframe(df,schema,drop_cols): # TODO update this to use "curated" "shared" or "raw" instead of full frame name
        '''
        Cleans a dataframe queried directly from the database.
        '''
        # change the time column name
        global time_columns
        df = df.rename(columns={time_columns[schema]: 'time'})

        # use a DatetimeIndex
        df['time'] = pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M:%S')
        # get some info about times
        start_time = df['time'][0]
        end_time = df['time'][len(df['time'])-1]
        step_size = df['time'][1]-start_time # will error out if we only have one time point
        times = (start_time, end_time, step_size)
        df.set_index('time', inplace=True)
        
        
        
        # drop unnecessary columns
        df = df.drop(['dataid'], axis=1)
        if schema == 'curated':
            df = df.drop(['id'], axis=1)
        if len(drop_cols)!=0:
            df= df.drop(drop_cols,axis=1)
        
        return (df, times)


def check_sample_rate(schema,sampling_rate):
        ##get from the data directly not like this
        accepted_rates = {'curated':'15T' ,'raw':'15' ,'shared':'1T' }

def get_month_traces(schema,table,dataid):
        # TODO change this name
        global schema_names,invalid_columns,source
        if schema not in ['curated','raw','shared']:
            raise SchemaError(schema)
        schema_name = schema_names[schema]
        query = 'select * from "{0}".{1} where dataid={2}'.format(schema_name, table, dataid)
        # TODO NEED TO CHANGE IDS
        # TODO error checking that query worked
        df = get_dataframe(query).fillna(0)

        df,times = clean_dataframe(df, schema,[])
        traces = []
        for col in df.columns:
            if not col in invalid_columns[schema]:
                s = pd.Series(df[col],name = col)
                meta={'source':source,'schema':schema,'table':table ,'dataid':dataid, 'start_time': times[0],'end_time':times[1], 'step_size':times[2] }
                traces.append(ApplianceTrace(s,meta))
        return traces

def get_month_traces_helper(schema,year,month,group=None):
    pass


def get_single_app_trace_need_house_id(house_df, app):
        '''by house is fastest also have get all apps below'''
        pass

def get_app_traces_all(schema,table,app,ids):
        global schema_names, source
        schema_name = schema_names[schema]
        traces = []
        for i in ids:
            query= 'select {2}, {4} from "{0}".{1} where dataid={3}'.format(schema_name,table,app,i,time_columns[schema])
            df=get_dataframe(query)
        #df = df.groupby('dataid')
       
            df = df.rename(columns={time_columns[schema]: 'time'})
            df['time'] = pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M:%S')
            df.set_index('time', inplace=True)
            meta = {'source':source,'schema':schema,'table':table ,'dataid':i}
            s = pd.Series(df[app],name = app)
            traces.append(ApplianceTrace(s,meta))
        ##well it's really a type right?
        # TODO - does this need to be cleaned differently?
        return traces

def get_type(schema,table,app):
    pass
# df = get_app_traces_all(schema,table,app)


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
