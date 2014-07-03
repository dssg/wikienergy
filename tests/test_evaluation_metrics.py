import sys
sys.path.append('../')
from disaggregator import evaluation_metrics as evm

import unittest
import numpy as np

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

if __name__ == '__main__':
    unittest.main()
