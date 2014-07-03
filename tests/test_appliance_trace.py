import sys
sys.path.append('..')
import disaggregator as da
import unittest
import pandas as pd
import numpy as np

class ApplianceTraceTestCase(unittest.TestCase):

    def setUp(self):
        index = pd.date_range('1/1/2013', periods=200, freq='15T')
        data = np.zeros(200)
        series = pd.Series(data, index=index)
        self.normal_trace = da.ApplianceTrace(series,{})

    def test_get_metadata(self):
        self.assertIsInstance(self.normal_trace.get_metadata(),dict,
                              'metadata should be a dict')

    def test_get_sampling_rate(self):
        self.assertEqual(self.normal_trace.get_sampling_rate(),'15T',
                         'sampling rate of test should be "15T"')

    def test_get_series(self):
        self.assertIsInstance(self.normal_trace.get_series(),pd.Series,
                              'series should be pd.Series')
        self.assertIsInstance(self.normal_trace.get_series().index,
                              pd.DatetimeIndex,
                              'trace series index should be pd.DatetimeIndex')

if __name__ == "__main__":
    unittest.main()
