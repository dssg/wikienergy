import psycopg2
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import *
import xlwt 




class GetDF:

    def __init__(self,query,url,dataids):
     
        eng = create_engine(url)
        eng.echo=True
        eng_object=eng.execute(query)
        df = pd.DataFrame.from_records(eng_object.fetchall())
        df.columns = eng_object.keys()
    #url = "postgresql"+"://"+user_name+":"+pw+"@"+host+":"+port+"/"+db
        dfs_dict = {}
        dfs=df.groupby('dataid')
        for df in dfs:
            df[1].drop('dataid',1)
            #df[1].drop('id',1)
            if df[0] in dataids.keys():
                dfs_dict[df[0]]=df[1]
        self.dfs_dict=dfs_dict
