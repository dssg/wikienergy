class ApplianceInstance(object):

    def __init__(self,traces):
        self.traces = traces

    def get_traces(self):
        return self.traces

    def add_trace(self):
        pass # make sure that the trace doesn't overlap with other traces
