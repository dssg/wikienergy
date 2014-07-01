import pandas

class ApplianceTrace(object):

    def __init__(self, series, source):
        '''
        Initializes a trace object from a series and a source.
        Series must be sampled at a particular sample rate
        '''
        self.series = series
        self.source = source

    def get_sampling_rate(self):
        '''
        Returns a string representing the rate at which the series was sampled.
        '''
        return self.series.index.freq

    def get_series(self):
        '''Returns the pandas series object representing this trace.'''
        return self.series

    def get_source(self):
        '''Returns the user-supplied trace source string.'''
        return self.source

    def set_series(self,series):
        '''Updates the series (such as after a resampling)'''
        self.series = series

    def set_source(self,source):
        '''Updates the user-supplied source string.'''
        self.source = source
