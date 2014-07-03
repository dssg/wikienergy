import sys
sys.path.append('../')
from disaggregator import PecanStreetDatasetAdapter as pecan

import unittest


class PecanStreetDatasetAdapterTestCase(unittest.TestCase):

    def setUp(self):
        db_url = "postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres"
        self.p = pecan(db_url)

    def test_get_table_names(self):
        #tables = self.p.get_table_names('shared')
        pass

    def test_table_metadata(self):
        #tables = self.p.get_table_names('shared')
        #i,a = p.get_table_metadata('shared',str(tables[0]))
        pass

    def test_get_month_traces(self):
        #traces = p.get_month_traces('SharedData',tables[0])
        #trace = p.get_month_traces_wo_time_align('shared',str(tables[0]),i[0])
        pass

if __name__ == '__main__':
    unittest.main()
