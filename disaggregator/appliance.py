import numpy as np
import pandas as pd
import pprint
from utils import order_traces

class ApplianceTrace(object):

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

    def get_total_usage(self):
        '''
        Returns the total usage of this trace
        '''
        return self.series.sum()

    def print_trace(self):
        '''
        Prints a summary of the trace
        '''
        print 'Series size: {}'.format(self.series.size)
        print 'Sampling rate: {}'.format(self.get_sampling_rate)
        print 'Metadata: '
        pprint.pprint(self.metadata)



class ApplianceInstance(object):

    def __init__(self,traces,metadata):
        '''Initialize an appliance trace with a list of traces'''
        self.traces = order_traces(traces)
        self.metadata=metadata

    def add_traces(self,traces):
        '''
        Updates the list of traces to include the traces in the newly supplied
        list of traces.
        '''
        pass # make sure that the trace doesn't overlap with other traces

    def concatenate_traces(self, how="strict"):
        '''
        Takes its own list of traces and attempts to concatenate them.
        '''
        if how == "strict":
            self.traces = [pd.concat(traces)]
        else:
            raise NotImplementedError


class ApplianceSet(object):

    def __init__(self,instances):
        '''
        Initializes an appliance set given a list of instances.
        '''
        self.instances = instances
        self.make_dataframe()

    def add_instances(self,instances):
        '''
        Adds the list of appliances to the appliance set.
        '''
        self.instances += instances
        self.add_to_dataframe(instances)

    def add_to_dataframe(self,instances):
        '''
        Adds a new list of appliances to the dataframe.
        '''
        pass

    def get_dataframe(self):
        '''
        Returns the dataframe object representing the dataset.
        '''
        return self.df

    def make_dataframe(self):
        '''
        Makes a new dataframe of the appliance instances. Throws an exception if
        if the appliance instances have traces that don't align.
        '''
        # TODO concatenate all traces into a single trace
        # TODO use real column_name
        series_dict = {"column_name":instance.traces[0].series for instance in instances}
        self.df = pd.Dataframe.from_dict(series_dict)

    def set_instances(self,instances):
        '''
        Replaces the old instances with the new list. Makes a new dataframe
        using those instances
        '''
        self.instances = instances
        self.make_dataframe()

    def top_k(self):
        '''
        Get top k energy-consuming appliances
        '''
        pass

class ApplianceType(object):

    def __init__(self, instances):
        '''
        Initialize a type object with a list of instances. (Check for
        uniqueness?)
        '''
        # TODO Check for uniqueness?
        self.instances = instances

    def add_instances(self,instances):
        '''
        Add instances to the list of instances. (Check for uniqueness?)
        '''
        # TODO Check for uniqueness?
        self.instances += instances

    def get_instances(self):
        '''
        Returns the list of appliance instances which are members of this type.
        '''
        return self.instances

    def set_instances(self,instances):
        '''
        Replaces the old list of instances with the new set of instances.
        (Check for uniqueness?)
        '''
        # TODO Check for uniqueness?
        self.instances = instances

