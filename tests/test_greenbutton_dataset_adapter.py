import sys
import os.path
sys.path.append(os.path.abspath(os.pardir))
from disaggregator import GreenButtonDatasetAdapter as gbda

import unittest


class GreenButtonDatasetAdapterTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_zipcode(self):
        zip_code=gbda.get_zipcode('<?xml version="1.0" ?><entry><title type="text">822 S LOMBARD AVE OAK PARK IL 60304-1610</title></entry>')
        self.assertEqual(zip_code,'60304')

if __name__ == '__main__':
    #unittest.TestRunner().run(fast)
    unittest.main()

