import pandas
import pprint

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
