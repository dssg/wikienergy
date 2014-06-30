from ApplianceTrace import ApplianceTrace
from ApplianceInstance import ApplianceInstance
from ApplianceType import ApplianceType
from ApplianceSet import ApplianceSet

import sqlalchemy
import pandas

class PecanStreetDatasetAdapter(object):

    def __init__(self,db_url):
        '''
        Initialize an adapter using a database url_string.
        Consider the following example:
        db_url="postgresql"+"://"+user_name+":"+ps+"@"+host+":"+port+"/"+db
        '''
        self.eng = sqlalchemy.create_engine(db_url)

    def get_unique_dataids(self,schema,month,group=None):
        '''
        Returns a list of dataids for a specifc schema ("curated","shared", or
        "raw"), month (int), year (int), and group (int).
        '''
        if schema == "curated":
            query = 'select distinct dataid from "PecanStreet_CuratedSets".group{0}_disaggregated_2013_{1:02d}'.format(group,month)
            eng_object = self.eng.execute(query)
            df = pandas.DataFrame.from_records(eng_object.fetchall())
            return list(df[0])
        elif schema == "shared":
            raise NotImplementedError
        elif schema == "raw":
            raise NotImplementedError
        else:
            raise NonexistentSchemaError

    def getApplianceTraces(self,schema,group):
        '''
        Returns traces for the specified time and sampling rate. Specify
        sampling rate using pandas offset aliases (Ex. 15 mins -> "15T")
        '''
        pass

