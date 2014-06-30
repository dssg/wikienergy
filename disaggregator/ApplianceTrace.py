import pandas

class ApplianceTrace(object):

    def __init__(self, series, source):
        '''
        Initializes a trace object from a series and a source.
        Series must be sampled at a particular sample rate
        '''
        self.series = series
        self.source = source

    def get_series(self):
        return self.series

    def get_source(self):
        return self.series

    def get_sampling_rate(self):
        return self.series.index.freq
