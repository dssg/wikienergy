import sys
sys.path.append('../')
from disaggregator import PecanStreetDatasetAdapter

import unittest


class PecanStreetDatasetAdapterTestCase(unittest.TestCase):

    def setUp(self):
        db_url = "postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres"
        self.psda = PecanStreetDatasetAdapter(db_url)

    def test_get_table_names(self):
        s_tables = self.psda.get_table_names('shared')
        c_tables = self.psda.get_table_names('curated')
        r_tables = self.psda.get_table_names('raw')
        self.assertIn('group1_disaggregated_2012_12', c_tables,
                      'curated schema has correct tables')
        self.assertIn('egauge_15min_2013', r_tables,
                      'raw schema has correct tables')
        self.assertIn('validated_01_2014', s_tables,
                      'shared schema has correct tables')

    def test_table_metadata(self):
        ids,cols = self.psda.get_table_metadata('shared','validated_01_2014')
        self.assertIn(744,ids,'shared table 01 2014 has dataid 744')
        self.assertIn('use',cols,'shared table 01 2014 has column "use"')
        self.assertIn('air1',cols,'shared table 01 2014 has column "air1"')
        pass

    def test_get_month_traces(self):
        # traces = self.pdsa.get_month_traces('shared','validated_01_2014')
        # trace = p.get_month_traces_wo_time_align('shared',str(tables[0]),i[0])
        pass

fast = TestSuite()

if __name__ == '__main__':
    unittest.main()
