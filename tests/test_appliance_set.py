import sys
import os.path
sys.path.append(os.path.abspath(os.pardir))
import disaggregator as da
import unittest
import pandas as pd
import numpy as np

class ApplianceSetTestCase(unittest.TestCase):

    def setUp(self):
        instances = []
        for i in range(3):
            index = pd.date_range('1/1/2013', periods=200, freq='15T')
            data = np.zeros(200)
            series = pd.Series(data, index=index)
            instances.append(da.ApplianceInstance([da.ApplianceTrace(series,{})],{}))
        self.normal_set = da.ApplianceSet(instances,{})

    def test_alignment(self):
        self.assert_(da.instances_aligned(self.normal_set.instances))

if __name__ == "__main__":
    unittest.main()
