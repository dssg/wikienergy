import appliance
import pandas as pd
import numpy as np
import csv
import glob
import os
from datetime import datetime
import decimal
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

    def get_trace_dates_from_instance(self,device,instance):
        '''
        This function returns a unique set of dates (corresponding to
        individual files) for a single device instance id
        '''
        trace_dates=set()
        for filename in glob.glob(self.path+device+'/dev_'+instance+'*'):
            instance_name_trace_date= filename[filename.index('dev_')+4:]
            trace_date=instance_name_trace_date[instance_name_trace_date\
                .index('_')+1:]
            trace_dates.add(trace_date[:trace_date.index('.csv')])
        return list(trace_dates)

    def map_to_decimal(self,floatVal):
        '''
        This function casts a value as a decimal. It is used specifically
        for the .map function when an entire series needs to be casted to 
        a decimal.
        '''
        return decimal.Decimal(floatVal)

    def generate_traces(self,device,instance_id,date):
        '''
        Returns trace:
	    series: indexed by time with column name 'time',
            series is series of average power value
        '''
        filename=self.path+device+'/dev_'+instance_id+'_'+date+'.csv'
        df = pd.read_csv(filename,sep=';',\
                header=None,names=['time','1s_W','8s_W'])
        df['time']=pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M:%S')
        df.set_index('time', inplace=True)
        try:
	    series=df['1s_W'].resample(self.sample_rate,how='sum')/3600.0
            series=series.map(self.map_to_decimal)
            series.name=device
        except ValueError:
	    raise SampleError(self.sample_rate)
        series_mult=self.split_on_NANs(series)
        return [ApplianceTrace(single_series,{'source':self.source,
            'device_name':device,'instance_name':instance_id ,'date':date,
            'trace_num':i}) for i,single_series in enumerate(series_mult)]

    def split_on_NANs(self,series):
        '''
        This function splits a trace into several traces, 
        divided by the NAN values. Only outputs traces that have at 
        least 6 hours of real values
        '''
        nan_indices=series[series.isnull()].index
        series_mult=[]
        prev_index=0
        if(nan_indices.size>0):
            for nan_index in nan_indices:
                series_sect=series[prev_index:nan_index]
                if(series_sect.size>26):
                    series_mult.append(series_sect[prev_index:nan_index]\
                        .dropna())
                prev_index=nan_index
        else:
            series_mult=[series]
        return series_mult

    def generate_instance(self,device,instance_id):
        '''
        This function imports the CSV files from a single device 
        instance in a device folder
        '''
        instance=[]
        instance_dates=self.get_trace_dates_from_instance(device,instance_id)
        for date in instance_dates:
            for trace in self.generate_traces(device,instance_id,date):
                instance.append(trace)

        meta={
            'source':self.source,
            'device_name':device,
            'instance_name':instance_id}
        return ApplianceInstance(instance,meta)

    def generate_type(self,device):
        '''
        This function imports the CSV files from ALL device instances
        in a single device folder
        '''
        device_type=[]
        instance_ids=self.get_unique_instance_ids(device)
        for instance_id in instance_ids:
	    device_type.append(self.generate_instance(device,instance_id))
        meta= {
            'source':self.source,
            'device_name':device}
        return ApplianceType(device_type,meta)

    def get_unique_instance_ids(self,device):
        '''
        This function returns a unique set of instance ids from tracebase
        '''
        instance_names=set()
        for filename in glob.glob(self.path+device+'/*'):
            instance_name_trace_date= filename[filename.index('dev_')+4:]
            underscore_index=instance_name_trace_date.index('_')
            instance_names.add(instance_name_trace_date[:underscore_index])
        return list(instance_names)

    def map_to_decimal(self,floatVal):
        '''
        This function casts a value as a decimal. It is used specifically
        for the .map function when an entire series needs to be casted to 
        a decimal.
        '''
        return decimal.Decimal(floatVal)

class SampleError(Exception):
    """

    Exception raised for errors in the re-sampling of the data.

    """
    def __init__(self,sample_rate):
        self.sample_rate = sample_rate

    def __str__(self):

        return '''Improperly formatted sampling rate.
            Check http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
            for proper formats.  Ex) For 15 minute sampling, do 15T'''
