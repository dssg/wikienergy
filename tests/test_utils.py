import sys
import os.path
sys.path.append(os.path.abspath(os.pardir))
import disaggregator as da
import unittest

class UtilsTestCase(unittest.TestCase):

    def setUp(self):
        pass

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

if __name__ == "__main__":
    unittest.main()
