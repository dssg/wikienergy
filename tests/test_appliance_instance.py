import sys
sys.path.append('..')
import disaggregator as da
import unittest
import pandas as pd
import numpy as np

class ApplianceInstanceTestCase(unittest.TestCase):

    def setUp(self):
        indices = [pd.date_range('1/1/2013', periods=96, freq='15T'),
                   pd.date_range('1/2/2013', periods=96, freq='15T')]
        data = [np.zeros(96),np.zeros(96)]
        series = [pd.Series(d, index=i) for d,i in zip(data,indices)]
        self.traces = [da.ApplianceTrace(s,{}) for s in series]
        self.normal_instance = da.ApplianceInstance(self.traces)

    def test_get_traces(self):
        self.assertIsNotNone(self.normal_instance.get_traces(),
                      'instance should have traces')

    def test_traces_in_order(self):
        traces = self.normal_instance.get_traces()
        self.assertLess(traces[0].series.index[0],
                        traces[1].series.index[0],
                        'traces should be in order')

    def test_traces_should_not_overlap(self):
        traces = self.normal_instance.get_traces()
        times = set()
        for trace in traces:
            for time in trace.series.index:
                self.assertNotIn(time, times,
                                 'traces should not overlap')
                times.add(time)

if __name__ == "__main__":
    unittest.main()
