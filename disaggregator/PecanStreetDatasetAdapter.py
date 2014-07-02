from ApplianceTrace import ApplianceTrace

import sqlalchemy
import pandas as pd

class PecanStreetDatasetAdapter():

    schema_names =    {'curated': '\"PecanStreet_CuratedSets\"',
                       'raw':     '\"PecanStreet_RawData\"',
                       'shared':  '\"PecanStreet_SharedData\"'}

    time_columns =    {'curated': 'utc_15min',
                       'raw':     'localminute15minute',
                       'shared':  'localminute'}

    invalid_columns = {'curated': ['id', 'utc_15min'],
                       'raw':     ['localminute15minute'],
                       'shared':  ['localminute']}

    def __init__(self,db_url):
        '''
        Initialize an adapter using a database url_string.
        Consider the following example:
        db_url="postgresql://user_name:password@host.url:port/db"
        '''
        self.eng = sqlalchemy.create_engine(db_url)
        self.source = "PecanStreet"

    def get_table_names(self,schema):
        '''
        Returns a list of tables in the schema.
        '''
        df = self.get_dataframe('select * from information_schema.tables')
        df = df.groupby(['table_schema','table_name'])
        groups = [group for group in df.groups]
        table_names = [t for (s,t) in groups if s == schema_names[schema]]
        return table_names

    def verify_same_range(self):
        '''
        Check that all data points have the same range
        '''
        pass

    def get_table_metadata(self,schema,table):
        '''
        Returns a tuple where the first element is a list of data ids for this
        schema.table and the second element is a list of the appliances
        included in this schema.table
        '''
        q = 'select distinct dataid from {}.{}'.format(schema_names[schema],table)
        result = self.eng.execute(q)
        ids = result.fetchall()
        q = 'select * from {}.{} where dataid={}'.format(schema_names[schema],table,ids[0][0])
        result = self.eng.execute(q)
        apps = result.keys()
        ids= [a[0] for a in ids]
        apps = [str(a) for a in apps ]
        return ids, apps

    def get_unique_dataids(self,schema,month,year,group=None):
        '''
        Returns a list of dataids for a specifc schema ("curated","shared", or
        "raw"), month (int), year (int), and group (int).
        '''
        if schema == "curated":
            schema_name = schema_names[schema]
            query = 'select distinct dataid from {0}.group{1}_disaggregated_{2}_{3:02d}'.format(schema_name,group,year,month)
            df = self.get_dataframe(query)
            return list(df["dataid"])
        elif schema == "shared":
            raise NotImplementedError
        elif schema == "raw":
            raise NotImplementedError
        else:
            raise SchemaError(schema)

    def get_month_traces(self,schema,year,month,dataid,group=None,sampling_rate="15T"):
        '''
        Returns a month-long traces for the specified month and sampling rate. Specify
        sampling rate using pd offset aliases (Ex. 15 mins -> "15T")
        '''
        if schema == "curated": # Lowest possible sampling rate is 15T
            # load dataframe and fill with zeros
            schema_name = schema_names[schema]
            query = 'select * from {0}.group{1}_disaggregated_{2}_{3:02d} where dataid={4}'.format(schema_name,group,year,month,dataid)
            df = self.get_dataframe(query).fillna(0)

            # column name for a trace series DatetimeIndex should be "time"
            df.rename(columns={'utc_15min': 'time'}, inplace=True)
            df.index = df['time'].apply(pd.to_datetime)

            # drop unneded columns
            df = df.drop(['id','dataid','time'], axis=1)

            # resample if necessary
            if not (sampling_rate == '15T' or sampling_rate == '15Min'):
                how = {col:'sum' for col in dataframe.columns}
                df = df.resample(sampling_rate, how=how)
        elif schema == "shared":
            pass
        elif schema == "raw":
            raise NotImplementedError
        else:
            raise SchemaError(schema)

        # make traces for each column
        traces = []
        for column, series in df.iteritems():
            traces.append(ApplianceTrace(series,self.source))
        return traces

    def time_align():
        '''Checks that for all traces in a home the total time lengths are the same'''
        pass

    def clean_dataframe(self,df,schema,drop_cols): # TODO update this to use "curated" "shared" or "raw" instead of full frame name
        '''
        Cleans a dataframe queried directly from the database.
        '''
        # change the time column name
        df = df.rename(columns={time_colums[schema]: 'time'})

        # use a DatetimeIndex
        df['time'] = pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M:%S')
        df.set_index('time', inplace=True)

        # get some info about times
        start_time = df['time'][0]
        end_time = df['time'][-1]
        step_size = df['time'][1]-start_time # will error out if we only have one time point
        times = (start_time, end_time, step_size)

        # drop unnecessary columns
        df = df.drop(['dataid'], axis=1)
        if schema == 'curated':
            df = df.drop(['id'], axis=1)
        if len(drop_cols)!=0:
            df= df.drop(drop_cols,axis=1)

        return df, times

    def check_sample_rate(self,schema,sampling_rate):
        ##get from the data directly not like this
        accepted_rates = {'curated':'15T' ,'raw':'15' ,'shared':'1T' }

    def get_month_traces_per_dataid(self,schema,table,dataid):
        # TODO change this name
        if schema not in ['curated','raw','shared']:
            raise SchemaError(schema)
        schema_name = schema_names[schema]
        query = 'select * from {0}.{1} where dataid={2}'.format(schema_name, table, dataid)
        # TODO NEED TO CHANGE IDS
        # TODO error checking that query worked
        df = self.get_dataframe(query).fillna(0)

        df,times = self.clean_dataframe(df, schema,[])
        traces = []
        for col in df.columns:
            if not col in invalid_columns[schema]:
                meta={'source':self.source,'schema':schema,'table':table ,'dataid':dataid, 'start_time': times[0],'end_time':times[1], 'step_size':times[2] }
                traces.append(ApplianceTrace(df[col],meta))
        return traces

    def get_single_app_trace_need_house_id(self,house_df, app):
        '''by house is fastest also have get all apps below'''
        pass

    def get_app_traces_all(self,schema,table,app):
        schema_name = schema_names[schema]
        query= 'select {2} from {0}.{1}'.format(schema_name,table,app)
        df=self.get_dataframe(query)
        # TODO - does this need to be cleaned differently?

    def get_dataframe(self,query):
        '''
        Returns a Pandas dataframe with the query results
        '''
        eng_object = self.eng.execute(query)
        df = pd.DataFrame.from_records(eng_object.fetchall())
        df.columns = eng_object.keys()
        return df

class SchemaError(Exception):
    '''Exception raised for errors in the schema.

        Attributes:
            schema  -- nonexistent schema
    '''
    def __init__(self,schema):
        self.schema = schema

    def __str__(self):
        return "Schema {} not supported or nonexistent.".format(self.schema)
