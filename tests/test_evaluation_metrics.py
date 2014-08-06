import sys
import os.path
sys.path.append(os.path.abspath(os.pardir))
from disaggregator import evaluation_metrics as evm
from disaggregator import appliance as app

import unittest
import numpy as np
import pandas as pd


class EvaluationMetricsTestCase(unittest.TestCase):

    def setUp(self):
        n = 7
        self.truth = np.ones(n)
        self.prediction = np.zeros(n)

    def test_sum_squared_residuals(self):
        self.assertEqual(evm.rss(self.truth,self.prediction), 7,
                         'incorrect sum of squared residuals')

    def test_sum_error(self):
        self.assertEqual(evm.sum_error(self.truth,self.prediction), 7,
                         'incorrect sum of error')

    def test_get_specificity(self):
        #stats =  evm.get_positive_negative_stats([1],[1])
        #print stats[0]
        #print stats[1]
        #print evm.get_specificity(stats[0],stats[1])
        pass

    def test_truth_from_power(self):
        #print evm.guess_truth_from_power(np.array([2,3,4,51,2]),3)
        pass

    def test_fraction_energy_assigned_correctly(self):
        traces = [[1,1,1,1,1],[5,5,5,5,5],[0,0,0,0,0]]
        p_traces = [[1,1,1,1,1],[5,5,5,5,5],[0,0,0,0,0]]
        meta = {'source':'test',
            'schema':'test_schema',
            'table':'test_table',
            'dataid':'test_id',
            'device_name':'',
        }
        traces = [app.ApplianceTrace(pd.Series(t),meta) for t in traces]
        for i,t in enumerate(traces):
            traces[i].metadata['device_name']==i
        p_traces =[app.ApplianceTrace(pd.Series(t),meta) for t in p_traces]
        for i,t in enumerate(p_traces):
            p_traces[i].metadata['device_name']==i
        meta_i = meta.pop('dataid')
        instance_p = app.ApplianceInstance(p_traces, meta_i)
        instance_t = app.ApplianceInstance(traces, meta_i)
        evm.fraction_energy_assigned_correctly(instance_p,instance_t)

    def test_get_table_of_confusion(self):
        stats = {'tp':np.array([1,1]),
                 'fp':np.array([0,0]),
                 'fn':np.array([0,0]),
                 'tn':np.array([0,0])}
        evm.get_table_of_confusion(stats)

if __name__ == '__main__':
    unittest.main()
