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
        self.assertDictEqual(self.normal_trace.get_metadata(),{})

if __name__ == "__main__":
    unittest.main()
