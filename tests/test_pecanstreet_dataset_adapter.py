import sys
import os.path
sys.path.append(os.path.abspath(os.pardir))
from disaggregator import PecanStreetDatasetAdapter as psda

import settings
import unittest


class PecanStreetDatasetAdapterTestCase(unittest.TestCase):

    def setUp(self):
        psda.set_url(settings.PECAN_STREET_DB_URL)

    def test_get_table_names(self):
        s_tables = psda.get_table_names('shared')
        c_tables = psda.get_table_names('curated')
        r_tables = psda.get_table_names('raw')
        self.assertIn('group1_disaggregated_2012_12', c_tables,
                      'curated schema has correct tables')
        self.assertIn('egauge_15min_2013', r_tables,
                      'raw schema has correct tables')
        self.assertIn('validated_01_2014', s_tables,
                      'shared schema has correct tables')

    def test_table_metadata(self):
        ids,cols = psda.get_table_dataids_and_column_names('shared','validated_01_2014')
        self.assertIn(744,ids,'shared table 01 2014 has dataid 744')
        self.assertIn('use',cols,'shared table 01 2014 has column "use"')
        self.assertIn('air1',cols,'shared table 01 2014 has column "air1"')
        pass

    def test_get_month_traces(self):
        # traces = self.pdsa.get_month_traces('shared','validated_01_2014')
        # trace = p.get_month_traces_wo_time_align('shared',str(tables[0]),i[0])
        pass

#fast = unittest.TestSuite()
#fast.addTest(PecanStreetDatasetAdapterTestCase.test_get_table_names)

if __name__ == '__main__':
    #unittest.TestRunner().run(fast)
    unittest.main()
