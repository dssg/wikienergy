import unittest
from test_evaluation_metrics import EvaluationMetricsTestCase
from test_appliance_trace import ApplianceTraceTestCase
from test_appliance_instance import ApplianceInstanceTestCase
from test_appliance_set import ApplianceSetTestCase
from test_appliance_type import ApplianceTypeTestCase
from test_utils import UtilsTestCase
from test_pecanstreet_dataset_adapter import PecanStreetDatasetAdapterTestCase

def suite():
    ev_m_suite =\
        unittest.TestLoader().loadTestsFromTestCase(EvaluationMetricsTestCase)
    a_tr_suite =\
        unittest.TestLoader().loadTestsFromTestCase(ApplianceTraceTestCase)
    a_in_suite =\
        unittest.TestLoader().loadTestsFromTestCase(ApplianceInstanceTestCase)
    a_st_suite =\
        unittest.TestLoader().loadTestsFromTestCase(ApplianceSetTestCase)
    a_ty_suite =\
        unittest.TestLoader().loadTestsFromTestCase(ApplianceTypeTestCase)
    util_suite =\
        unittest.TestLoader().loadTestsFromTestCase(UtilsTestCase)

    psda_tests = [
        'test_get_table_names',
        'test_get_month_traces',
    ]
    psda_suite =\
        unittest.TestSuite(map(PecanStreetDatasetAdapterTestCase, psda_tests))

    all_tests = unittest.TestSuite([
        ev_m_suite,
        a_tr_suite,
        a_in_suite,
        a_st_suite,
        a_ty_suite,
        util_suite,
        psda_suite,
    ])

    return all_tests

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
