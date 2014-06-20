```python

import pywapi
import urllib2
import json
import pandas as pd


def get_current_temp(city = None,state = None, zipcode = None):
    if(zipcode == None):
        query = 'http://api.zippopotam.us/us/'+state+'/'+city+''
        f = urllib2.urlopen(query)
        json_string = f.read()
        parsed_json = json.loads(json_string)
        #grab the zipcode of the first json object
        z = parsed_json['places'][0]['post code']
        #query the returned zip code from the city
        weather_com_result = pywapi.get_weather_from_weather_com(z)
        temp_c = weather_com_result['current_conditions']['temperature']
        temp_f = int(temp_c) * (1.8) + 32        
        return temp_f
    if(zipcode != None):
        weather_com_result = pywapi.get_weather_from_weather_com(zipcode)
        temp_c = weather_com_result['current_conditions']['temperature']
        temp_f = int(temp_c) * (1.8) + 32
        return temp_f

j = get_current_temp('oak park','IL')
print j 

```