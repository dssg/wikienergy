from ApplianceTrace import ApplianceTrace

import sqlalchemy
import pandas

class PecanStreetDatasetAdapter():
    def __init__(self,db_url):
        '''
        Initialize an adapter using a database url_string.
        Consider the following example:
        db_url="postgresql"+"://"+user_name+":"+ps+"@"+host+":"+port+"/"+db
        '''
        self.eng = sqlalchemy.create_engine(db_url)
    # self.source = "PecanStreet"
    
    def set_table_names(self,schema):
        ''''''
        df = self.get_dataframe('select * from information_schema.tables')
        df=(df.groupby(['table_schema','table_name']))
        d = [k for k in df.groups]
        tables = [l[1] for l in d if l[0]==schema]
        return tables
    
    
    def verify_same_range():
        '''check that all data points have the same range'''
        pass
    
    def get_meta_table(self,schema,table):
        '''would prefer that this be a class that these be attributes'''
        return self.get_list('select distinct dataid from {}.{}'.format(schema,table))
        # date_start =
        # date_end =
        # step_size =
    
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
        sampling rate using pandas offset aliases (Ex. 15 mins -> "15T")
        '''
        if schema == "curated":
            # Lowest possible sampling rate is 15T
            query = 'select * from "PecanStreet_CuratedSets".group{0}_disaggregated_{1}_{2:02d} where dataid={3}'.format(group,year,month,dataid)
            df = self.get_dataframe(query).fillna(0)
            df.rename(columns={'utc_15min': 'time'}, inplace=True)
            df.index = df['time'].apply(pandas.to_datetime)
            df = df.drop(['id','dataid','time'], axis=1)
            if not (sampling_rate == '15T' or sampling_rate == '15Min'):
                how = {col:'sum' for col in dataframe.columns}
                df = df.resample(sampling_rate, how=how)
        elif schema == "shared":
            raise NotImplementedError
        elif schema == "raw":
            raise NotImplementedError
        else:
            raise SchemaError(schema)
        traces = []
        for column, series in df.iteritems():
            traces.append(ApplianceTrace(series,self.source))
        return traces

    def get_dataframe(self,query):
        '''Returns a pandas dataframe with the query results'''
        eng_object = self.eng.execute(query)
        df = pandas.DataFrame.from_records(eng_object.fetchall())
        df.columns = eng_object.keys()
        return df

    def get_list(self,query):
        result  = self.eng.execute(query).fetchall()
        return result


class SchemaError(Exception):
    """Exception raised for errors in the schema.

        Attributes:
            schema  -- nonexistent schema
    """
    def __init__(self,schema):
        self.schema = schema

    def __str__(self):
        return "Schema {} not supported or nonexistent.".format(self.schema)
