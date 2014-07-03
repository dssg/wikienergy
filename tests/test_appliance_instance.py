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

if __name__ == "__main__":
    unittest.main()
