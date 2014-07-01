import numpy as np

class ApplianceInstance(object):

    def __init__(self,traces):
        '''Initialize an appliance trace with a list of traces'''
        self.traces = self.order_traces(traces)

    def add_traces(self,traces):
        '''
        Updates the list of traces to include the traces in the newly supplied
        list of traces.
        '''
        pass # make sure that the trace doesn't overlap with other traces

    def get_traces(self):
        '''
        Returns a reference to the list of traces owned by the appliance.
        '''
        return self.traces

    def set_traces(self):
        '''
        Sets the list of traces owned by the appliance
        '''
        self.traces = self.order_traces(traces)

    def order_traces(self,traces):
        '''
        Given a set of traces, orders them chronologically and catches
        overlapping traces.
        '''
        order = np.argsort([t.series[0] for t in traces])
        new_traces = [traces[i] for i in order]
        return new_traces
