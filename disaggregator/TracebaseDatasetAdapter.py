from ApplianceTrace import ApplianceTrace
from ApplianceInstance import ApplianceInstance
from ApplianceType import ApplianceType
from ApplianceSet import ApplianceSet

import sqlalchemy

class TracebaseDatasetAdapter(object):

    def __init__(self,db_url):
        '''
        Consider the following datapase:
        user_name = 'user'
        pw='password'
        host = "db.wiki-energy.org"
        port = "5432"
        db = "postgres"
        url = "postgresql"+"://"+user_name+":"+pw+"@"+host+":"+port+"/"+db

        '''
        self.eng = sqlalchemy.create_engine(db_url)
