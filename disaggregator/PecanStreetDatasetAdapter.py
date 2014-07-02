from ApplianceTrace import ApplianceTrace

import sqlalchemy
import pandas as pd

class PecanStreetDatasetAdapter():
    def __init__(self,db_url):
        '''
        Initialize an adapter using a database url_string.
        Consider the following example:
        db_url="postgresql"+"://"+user_name+":"+ps+"@"+host+":"+port+"/"+db
        '''
        self.eng = sqlalchemy.create_engine(db_url)
        self.source = "PecanStreet"

    def look_up_schema_map(self,schema):
        '''
        Gets the table name from the table shorthand name.
        '''
        table = {'curated':'\"PecanStreet_CuratedSets\"',
                'raw':'\"PecanStreet_RawData\"',
                'shared':'\"PecanStreet_SharedData\"'}
        return table[schema]

    def set_table_names(self,schema): #TODO Change this func name to "get_table_names"
        '''
        Returns a list of tables in the schema.
        '''
        df = self.get_dataframe('select * from information_schema.tables')
        df = df.groupby(['table_schema','table_name'])
        groups = [group for group in df.groups]
        table_names = [t for (s,t) in groups if s==schema]
        return table_names

    def verify_same_range(self):
        '''
        Check that all data points have the same range
        '''
        pass

    def get_meta_table(self,schema,table):
        '''
        Returns a tuple where the first element is a list of data ids for this
        schema.table and the second element is a list of the appliances
        included in this schema.table
        '''
        q = 'select distinct dataid from {}.{}'.format(schema,table)
        result = self.eng.execute(q)
        ids = result.fetchall()
        q = 'select * from {}.{} where dataid={}'.format(schema,table,ids[0][0])
        result = self.eng.execute(q)
        apps = result.keys()
        ids= [a[0] for a in ids]
        apps = [str(a) for a in apps ]
        return [ids,apps]

    def get_unique_dataids(self,schema,month,year,group=None):
        '''
        Returns a list of dataids for a specifc schema ("curated","shared", or
        "raw"), month (int), year (int), and group (int).
        '''
        if schema == "curated":
            query = 'select distinct dataid from "PecanStreet_CuratedSets".group{0}_disaggregated_{1}_{2:02d}'.format(group,year,month)
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
        if schema == "curated":
            # Lowest possible sampling rate is 15T
            query = 'select * from "PecanStreet_CuratedSets".group{0}_disaggregated_{1}_{2:02d} where dataid={3}'.format(group,year,month,dataid)
            df = self.get_dataframe(query).fillna(0)
            df.rename(columns={'utc_15min': 'time'}, inplace=True)
            df.index = df['time'].apply(pd.to_datetime)
            df = df.drop(['id','dataid','time'], axis=1)
            if not (sampling_rate == '15T' or sampling_rate == '15Min'):
                how = {col:'sum' for col in dataframe.columns}
                df = df.resample(sampling_rate, how=how)
        elif schema == "shared":
            pass
        elif schema == "raw":
            raise NotImplementedError
        else:
            raise SchemaError(schema)
        traces = []
        for column, series in df.iteritems():
            traces.append(ApplianceTrace(series,self.source))
        return traces
    
    ##do table work
    
    def time_align():
        '''Checks that for all traces in a home the total time lengths are the same'''
        pass
    
    def clean_dataframe(self,df,schema,drop_cols):
            time_cols = {'\"PecanStreet_CuratedSets\"':'utc_15min','\"PecanStreet_RawData\"':'localminute15minute','\"PecanStreet_SharedData\"':'localminute'}
            df=df.rename(columns={time_cols[schema]: 'time'})
            df['time']=pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M:%S')
            start_time = df['time'][0]
            end_time = df['time'][len(df['time'])-1]
            step_size = df['time'][1]-start_time
            df.set_index('time', inplace=True)
            #df = df.drop(['id','dataid','time'], axis=1)
            #print df.shape
            dataid = df['dataid'][0]
            df = df.drop(['dataid'], axis=1)
            if schema=='\"PecanStreet_CuratedSets\"':
                df = df.drop(['id'], axis=1)
            if len(drop_cols)!=0:
                df= df.drop(drop_cols,axis=1)
            times = [start_time,end_time, step_size]
            return [df,dataid,times]
    
    def invalid_col(self,col,schema):
        invalids={'\"PecanStreet_CuratedSets\"':['id','utc_15min'],'\"PecanStreet_RawData\"':['localminute15min'], '\"PecanStreet_SharedData\"':['localminute']}
        return col in invalids[schema]
    
    def check_sample_rate(self,schema,sampling_rate):
        ##get from the data directly not like this
        accepted_rates = {'curated':'15T' ,'raw':'15' ,'shared':'1T' }

    
    def get_month_traces_per_dataid(self,schema,table,dataid):
        ##change this name
        if schema not in ['\"PecanStreet_CuratedSets\"','\"PecanStreet_RawData\"','\"PecanStreet_SharedData\"']:
            raise SchemaError(schema)
        query = 'select * from {0}.{1} where dataid={2}'.format(schema, table,dataid)
        ##NEED TO CHANGE IDS
        ##error checking that query worked
        df = self.get_dataframe(query).fillna(0)
        
        [df,da,times] = self.clean_dataframe(df, schema,[])
        traces = []
        for col in df.columns:
            if not self.invalid_col(col,schema):
                meta={'source':self.source,'schema':schema,'table':table ,'dataid':da, 'start_time': times[0],'end_time':times[1], 'step_size':times[2] }
                traces.append(ApplianceTrace(df[col],meta))
        
        return traces

    def get_single_app_trace_need_house_id(self,house_df, app):
        '''by house is fastest also have get all apps below'''
        pass


    def get_app_traces_all(self,schema,table,app):
        query= 'select {2} from {0}.{1}'.format(schema,table,app)
        df=self.get_dataframe(query)
        ##does this need to be cleaned differently?




    def get_dataframe(self,query):
        '''Returns a pd dataframe with the query results'''
        eng_object = self.eng.execute(query)
        
        df = pd.DataFrame.from_records(eng_object.fetchall())
        df.columns = eng_object.keys()
        return df

    def get_list(self,query):
        result  = self.eng.execute(query).fetchall()
        return [result,result.keys()]


class SchemaError(Exception):
    """Exception raised for errors in the schema.

        Attributes:
            schema  -- nonexistent schema
    """
    def __init__(self,schema):
        self.schema = schema

    def __str__(self):
        return "Schema {} not supported or nonexistent.".format(self.schema)
