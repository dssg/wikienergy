import sys
import os.path
sys.path.append(os.path.abspath(os.pardir))
from disaggregator import weather
import datetime
import settings
import unittest
import pandas as pd

class WeatherTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_remove_low_outliers_df(self):
        base = datetime.datetime.today()
        date_list = [base - datetime.timedelta(days=x) for x in range(0, 5)]
        test=pd.DataFrame([-1000000,80,30,65,65],index=date_list,columns=['temp'])
        output=weather._remove_low_outliers_df(test,'temp')
        self.assertEqual(30,min(output['temp']))

if __name__ == '__main__':
    #unittest.TestRunner().run(fast)
    unittest.main()


