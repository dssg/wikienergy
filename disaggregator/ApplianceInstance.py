import numpy as np

class ApplianceInstance(object):

    def __init__(self,traces,metadata):
        '''Initialize an appliance trace with a list of traces'''
        self.traces = self.order_traces(traces)
        self.metadata=metadata

    def add_traces(self,traces):
        '''
        Updates the list of traces to include the traces in the newly supplied
        list of traces.
        '''
        pass # make sure that the trace doesn't overlap with other traces

    def order_traces(self,traces):
        '''
        Given a set of traces, orders them chronologically and catches
        overlapping traces.
        '''
        order = np.argsort([t.series[0] for t in traces])
        new_traces = [traces[i] for i in order]
        return new_traces
