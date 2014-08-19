import sys
import os.path
sys.path.append(os.path.abspath(os.pardir))
from disaggregator import GreenButtonDatasetAdapter as gbda

import unittest


class GreenButtonDatasetAdapterTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_zipcode(self):
        example_xml = [
            '<?xml version="1.0" ?><entry><title type="text">123 EXAMPLE AVE OAK PARK IL 60304-1234</title></entry>',
            '<?xml version="1.0" ?><entry><title type="text">OAK PARK IL 60305</title></entry>',
            ]
        answers = [
            '60304',
            '60305',
            ]
        for example, answer in zip(example_xml,answers):
            self.assertEqual(gbd.get_zipcode(example),zip_code,answer)

if __name__ == '__main__':
    #unittest.TestRunner().run(fast)
    unittest.main()

