from ApplianceTrace import ApplianceTrace
from ApplianceInstance import ApplianceInstance
from ApplianceType import ApplianceType
from ApplianceSet import ApplianceSet
import pandas as pd
import numpy as np
import csv
import glob
import os
from datetime import datetime
#####TO DO - incorporate TRACE_LENGTH
class TracebaseDatasetAdapter(object):

    def __init__(self,path,trace_length='D',sample_rate='15T'):
        '''
        Consider the following path:
        path = '/home/steve/DSSG/tracebase/complete/'
        trace_length='D', using Offset Aliases Pandas object notation
        sample_rate = "15T", using Offset Aliases Pandas object notation

        '''
        self.path=path
        self.sample_rate=sample_rate
        self.source='Tracebase'

    def generate_instance_dates(self,device,instance):
        '''
        This function returns a unique set of dates (corresponding to individual files) for a single device instance id

        '''
        trace_dates=set()
        for filename in glob.glob(self.path+device+'/dev_'+instance+'*'):
            instance_name_trace_date= filename[filename.index('dev_')+4:]
            trace_date=instance_name_trace_date[instance_name_trace_date.index('_')+1:]
            trace_dates.add(trace_date[:trace_date.index('.csv')])
        return list(trace_dates)

    def generate_trace(self,device,instance_id,date):
        '''
        Returns trace:
	    series: indexed by time with column name 'time', series is series of average power value

        '''   
        filename=self.path+device+'/dev_'+instance_id+'_'+date+'.csv'
        df = pd.read_csv(filename,sep=';',header=None,names=['time','1s_W','8s_W'])
        df['time']=pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M:%S')
        metadata={'source':self.source,'device_name':device,'instance_name':instance_id ,'date':date}
        df.set_index('time', inplace=True)	
        try:
	        series=df['1s_W'].resample(self.sample_rate,how='sum')/3600.0
        except ValueError:
	        raise SampleError(self.sample_rate)
		
        return ApplianceTrace(series,metadata)
        
    
    def generate_instance(self,device,instance_id):
        '''
        This function imports the CSV files from a single device instance in a device folder

        '''
        instance=[]
        instance_dates=self.generate_instance_dates(device,instance_id)
        for date in instance_dates:
            instance.append(self.generate_trace(device,instance_id,date))
        return ApplianceInstance(instance)

    
    def generate_type(self,device):
        '''
        This function imports the CSV files from ALL device instances in a single device folder

        '''
        device_type=[]
        instance_ids=self.generate_unique_instance_ids(device)
        for instance_id in instance_ids:
	         device_type.append(self.generate_instance(device,instance_id))
        return ApplianceType(device_type)

    def generate_unique_instance_ids(self,device):
        '''
        This function returns a unique set of instance ids from tracebase

        '''
        instance_names=set()
        for filename in glob.glob(self.path+device+'/*'):
            instance_name_trace_date= filename[filename.index('dev_')+4:]
            instance_names.add(instance_name_trace_date[:instance_name_trace_date.index('_')])
        return list(instance_names)
	

       
class SampleError(Exception):
    """

    Exception raised for errors in the re-sampling of the data.

    """
    def __init__(self,sample_rate):
        self.sample_rate = sample_rate

    def __str__(self):

        return "Improperly formatted sampling rate. Check http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases for proper formats.  Ex) For 15 minute sampling, do 15T"

