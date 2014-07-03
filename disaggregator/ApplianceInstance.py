import numpy as np
from pandas import concat
from utils import order_traces

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
            self.traces = [concat(traces)]
        else:
            raise NotImplementedError

