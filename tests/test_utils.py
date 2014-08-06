import sys
import os.path
sys.path.append(os.path.abspath(os.pardir))
import disaggregator as da
import pandas as pd
import numpy as np
import unittest
from datetime import datetime

class UtilsTestCase(unittest.TestCase):

    def setUp(self):
        self.consecutive_traces = []
        self.consecutive_instances = []
        for i in range(1,6):
            start = datetime(2013,1,i)
            series = pd.Series(np.zeros(24*4),
                    index=pd.date_range(start, periods=24*4, freq='15T'))
            trace = da.ApplianceTrace(series,{})
            self.consecutive_traces.append(trace)
            self.consecutive_instances.append(da.ApplianceInstance([trace],{}))
        self.piecewise_instance = da.ApplianceInstance(self.consecutive_traces,{})

    def test_get_common_ids(self):
        ids0 = []
        ids1 = [1,2,3]
        ids2 = [2,3,4,5,6]
        ids3 = [1,2,3,4,5,6,7]
        id_list1 = [ids0,ids3]
        id_list2 = [ids1,ids2]
        id_list3 = [ids2,ids3]
        common1 = da.get_common_ids(id_list1)
        common2 = da.get_common_ids(id_list2)
        common3 = da.get_common_ids(id_list3)
        self.assertListEqual([],common1)
        [self.assertIn(el,common2)    for el in [2,3]]
        [self.assertNotIn(el,common2) for el in [1,4]]
        [self.assertIn(el,common3)    for el in [2,5]]
        [self.assertNotIn(el,common3) for el in [1,7]]

    def test_aggregate_traces_misaligned(self):
        self.assertRaises(da.AlignmentError,
                          da.aggregate_traces,self.consecutive_traces,{})

    def test_aggregate_traces_aligned(self):
        aligned_traces = da.align_traces(self.consecutive_traces)
        da.aggregate_traces(aligned_traces,{})

    def test_aggregate_instances_misaligned(self):
        self.assertRaises(da.AlignmentError,
                          da.aggregate_instances,self.consecutive_instances,{})

    def test_aggregate_instances_aligned(self):
        aligned_instances = da.align_instances(self.consecutive_instances)
        da.aggregate_instances(aligned_instances,{})

    def test_concatenate_traces_consecutive(self):
        trace = da.concatenate_traces(self.consecutive_traces,{})
        self.assertEqual(trace.series.index.size, 24 * 4 * 5)

    def test_concatenate_instances_consecutive(self):
        instance = da.concatenate_instances(self.consecutive_instances,{})
        self.assertEqual(instance.traces[0].series.index.size, 24 * 4 * 5)

if __name__ == "__main__":
    unittest.main()
