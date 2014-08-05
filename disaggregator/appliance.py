"""
.. module:: appliance
   :platform: Unix
   :synopsis: Contains classes for representing appliances and appliance
      traces.

.. moduleauthor:: Phil Ngo <ngo.phil@gmail.com>
.. moduleauthor:: Miguel Perez <miguel@invalid.com>
.. moduleauthor:: Stephen Suffian <steve@invalid.com>
.. moduleauthor:: Sabina Tomkins <sabina.tomkins@gmail.com>

"""

import numpy as np
import pandas as pd
import pprint
from utils import order_traces
import utils
import decimal
import json

class ApplianceTrace(object):
    """This class represents appliance traces.

    Traces are power used by a single (or single set of) appliances sampled
    at a consistent rate.

    """

    def __init__(self, series, metadata):
        '''
        Initializes a trace object from a series and a metadata dictionary.
        Series must be sampled at a particular sample rate
        '''
        self.series = series
        self.metadata = metadata

    def get_sampling_rate(self):
        '''
        Returns a string representing the rate at which the series was sampled.
        '''
        return self.series.index.freq

    def get_time_of_day(self, start_time, end_time):
        '''
        Given a start and end datetime.time, it returns a trace
        within that time period.
        '''
        new_series = self.series.ix[start_time:end_time]
        return ApplianceTrace(new_series,self.metadata)

    def get_windows(self, window_length, window_step):
        """
        Returns a numpy array with stacked sliding windows of data.
        """
        total_length = self.series.size
        n_steps = int((total_length - window_length) / window_step)
        windows = []
        for step in range(n_steps):
            start = step * window_step
            window = self.series[start:start + window_length].tolist()
            windows.append(window)
        return np.array(windows,dtype=np.float)

    def get_total_usage(self):
        '''
        Returns the total usage of this trace
        '''
        return self.series.sum()

    def get_daily_usage(self):
        '''
        Returns the total daily usage of this trace
        '''
        return series.resample('D', how='mean')

    def print_trace(self):
        '''
        Prints a summary of the trace
        '''
        print 'Series size: {}'.format(self.series.size)
        print 'Sampling rate: {}'.format(self.get_sampling_rate)
        print 'Metadata: '
        pprint.pprint(self.metadata)

    def resample(self,sample_rate, method='mean'):
        '''
        Returns a new trace resampled to a given sample rate, defined by the
        offset aliases described in panda time series.
        http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
        '''
        try:
            new_series = self.series.astype(float)
            new_series = new_series.resample(sample_rate,how=method)
            new_series = new_series.fillna(0)
            new_series = new_series.map(decimal.Decimal)
            new_series.name = self.series.name
        except ValueError:
            raise utils.SampleError(sample_rate)
        return ApplianceTrace(new_series,self.metadata)

    def split_by(self,rate):
        '''
        Returns a list of traces formed by splitting this trace by day ('D')
        or week ('W')
        '''
        # set rate to group by
        if rate == 'D' or rate == '1D':
            groupby_rate = self.series.index.date
        elif rate == 'W' or rate == '1W':
            groupby_rate = self.series.index.week
        else:
            raise NotImplementedError('Looking for "week" or "day"')

        traces=[]
        for i, group in enumerate(self.series.groupby(groupby_rate)):
            metadata = dict.copy(self.metadata)
            metadata['trace_num'] = i
            traces.append(ApplianceTrace(group[1],metadata))
        return traces

    def to_daily_usage_json(self,method='utc_dict'):
        '''
        Returns the daily usage sum trace in a json format for calendar view
        '''
        d_sum = self.resample('D', 'sum')
        if method == 'utc_dict':
            data = {}            
            for i, v in d_sum.series.iteritems():
                kwh = v/1000
                unixtime = str(i.strftime("%s"))
                data.update({unixtime:float(kwh)})
        elif method == 'date_list':
            data = []
            for i, v in d_sum.series.iteritems():
                kwh = v/1000
                data.append({'date':i.strftime('%Y-%m-%d %H:%M'),
                             'usage': float(kwh)})
        else:
            raise NotImplementedError
        json_string = json.dumps(data, ensure_ascii=False)
        return json_string

    def to_json(self):
        '''
        Returns the trace in a json format amenable to d3 visualization.
        '''
        data = []
        for i, v in self.series.iteritems():
            data.append({'date':i.strftime('%Y-%m-%d %H:%M'),
                         'reading': float(v)})
        json_string = json.dumps(data, ensure_ascii=False,
                                 indent=4, separators=(',', ': '))
        return json_string


class ApplianceInstance(object):
    """
    This class represents appliance instances, which may have multiple
    appliance traces.

    Instances hold traces from a single instance of an appliance sampled
    at a consistent rate. Traces may or may not be consecutive.

    """


    def __init__(self,traces,metadata):
        '''Initialize an appliance trace with a list of ApplianceTraces'''
        self.traces = order_traces(traces)
        self.metadata=metadata

    def concatenate_traces(self, how="strict"):
        '''
        Takes its own list of traces and attempts to concatenate them.
        '''
        if how == "strict":
            self.traces = [pd.concat(traces)]
        else:
            raise NotImplementedError

    def get_time_of_day(self,start_time,end_time):
        '''
        Given a start and end datetime.time, it returns an instance with traces
        within that time period.
        '''
        new_traces = []
        for trace in self.traces:
            new_traces.append(trace.get_time_of_day(start_time,end_time))
        return ApplianceInstance(new_traces,self.metadata)

    def resample(self,sample_rate):
        '''
        Returns an instance with resampled traces.
        '''
        new_traces = []
        for trace in self.traces:
            new_traces.append(trace.resample(sample_rate))
        return ApplianceInstance(new_traces,self.metadata)

    def split_by(self,rate):
        '''
        Return a new ApplianceTrace in which each instance split into multiple
        traces split by day ('D') or week ('W') - (Sun-Sat?)
        '''
        traces=[]
        for trace in self.traces:
            traces.extend(trace.split_by(rate))
        return ApplianceInstance(traces,self.metadata)


class ApplianceSet(object):
    """
    This class represents appliance sets, which contain a set of temporally
    aligned appliance instances.

    Appliance sets are most frequently used as ground-truth for various
    algorithms, representing a particular home, building, or metered unit.

    """
    def __init__(self,instances,metadata):
        '''
        Initializes an appliance set given a list of instances.
        '''
        if not utils.instances_aligned(instances):
            self.instances = utils.align_instances(instances)
        else:
            self.instances = instances
        self.metadata = metadata

    def generate_top_k_set(self,k):
        '''
        Get top k energy-consuming appliances
        '''
        # TODO compare speeds of individual instance summing vs dataframe building and summing
        # TODO more intelligently create the metadata
        df = get_dataframe()
        total_usages = df.sum(axis=0)
        usage_order = np.argsort(total_usages)[::-1] # assumes correctly ordered columns
        top_k_instances = [self.instances[i] for i in usage_order[:k]]
        return ApplianceSet(top_k_instances,
                            {"name":"top_{}".format(k)})

    def generate_non_zero_set(self):
        '''
        Get all energy-consuming appliances (and drop instances with traces
        with all zeros)
        '''
        # TODO compare speeds of individual instance summing vs dataframe building and summing
        # TODO intelligently create the metadata
        df = get_dataframe()
        total_usages = df.sum(axis=0)
        usage_order = np.argsort(total_usages)[::-1] # assumes correctly ordered columns
        non_zero_instances = [self.instances[i] for i in usage_order if total_usages[i] > 0 ]
        return ApplianceSet(non_zero_instances,
                            {"name":"non_zero"})


    def get_dataframe(self):
        '''
        Makes a new dataframe of the appliance instances. Throws an exception if
        if the appliance instances have traces that don't align.
        '''
        # TODO concatenate all traces into a single trace
        # TODO change this to ordered dict
        # TODO actually throw an exception
        series_dict = {instance.traces[0].series.name:instance.traces[0].series
                       for instance in self.instances}
        return pd.DataFrame.from_dict(series_dict)

    def get_time_of_day(self,start_time,end_time):
        '''
        Given a start and end datetime.time, it returns an ApplianceType with
        traces within that time period.
        '''
        new_instances=[]
        for instance in self.instances:
            new_instances.append(instance.get_time_of_day(start_time,end_time))
        return ApplianceType(new_instances,self.metadata)
    def resample(self, sample_rate):
        '''
        Returns a new ApplianceSet instance with resampled traces.
        '''
        new_instances=[]
        for instance in self.instances:
            new_instances.append(instance.resample(sample_rate))
        return ApplianceSet(new_instances,self.metadata)

    def split_by(self, rate):
        '''
        Returns a new ApplianceSet object for which each trace in each instance
        is split into multiple traces from unique days ('D') or weeks ('W')
        '''
        instances = []
        for instance in self.instances:
            new_instance = instance.split_by(rate)
            instances.append(new_instance)
        return ApplianceSet(instances,self.metadata)

class ApplianceType(object):
    """This class represents appliance types, which contain a set of
    ApplianceInstances which share particular attributes, but which are not
    necessarily temporally aligned.

    Appliance types are most frequently used to generate models of particular
    types of appliances.
    """

    def __init__(self, instances, metadata):
        '''
        Initialize a type object with a list of instances. (Check for
        uniqueness?)
        '''
        # TODO Check for uniqueness?
        self.instances = instances
        self.metadata = metadata
        try:
            self.instance_id_index={instance.metadata['dataid']:i for i,instance in enumerate(instances)}
        except KeyError:
            print 'Warning: no "dataid" key found in metadata.'

    def get_instance_by_id(self,instance_id):
        '''
        Gets the instance of the type with a specified instance id
        '''
        index = self.instance_id_index[instance_id]
        return ApplianceType.instances[index]

    def get_time_of_day(self,start_time,end_time):
        '''
        Given a start and end datetime.time, it returns an ApplianceSet with
        traces within that time period.
        '''
        new_instances=[]
        for instance in self.instances:
            new_instances.append(instance.get_time_of_day(start_time,end_time))
        return ApplianceSet(new_instances,self.metadata)

    def resample(self,sample_rate):
        '''
        Returns a new ApplianceType with resampled traces.
        '''
        new_instances=[]
        for instance in self.instances:
            new_instances.append(instance.resample(sample_rate))
        return ApplianceType(new_instances,self.metadata)

    def split_by(self, rate):
        '''
        Returns a new ApplianceType object for which each trace in each instance
        is split into multiple traces from unique days ('D') or weeks ('W')
        '''
        instances=[]
        for instance in self.instances:
            new_instance= instance.split_by(rate)
            instances.append(new_instance)
        return ApplianceType(instances,self.metadata)

