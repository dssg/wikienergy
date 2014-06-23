#Get Weather Data
This ipython notebook uses the Weather Underground [API](http://www.wunderground.com/weather/api/d/docs) to grab weather data from particular cities in the US. The data is returned as a JSON object, and is read as a pandas dataframe for quick graphing. View notebook [here](http://nbviewer.ipython.org/github/mperez4/get_weather_data/blob/master/get_weather_data.ipynb)
```python
import json
import urllib2
import numpy as np
import pandas as pd
import collections 
import matplotlib.pyplot as plt
from scipy import stats
%matplotlib inline  
from datetime import datetime, timedelta, date


def get_weather_data(api,city,state,start_date,end_date):  
    if(start_date is not None and end_date is not None):

        #format our date structure to pass to our http request
        date_format = "%Y%m%d"
        a = datetime.strptime(start_date, date_format)
        b = datetime.strptime(end_date, date_format)
        #get number of days from start_date to end_date
        delta = b - a
        num_days = delta.days
        objects_list = []
    
        #create new variable that will create query's for the api
        for year in range(0,num_days + 1):
            #count from start_date to end_date
            dates = a + timedelta(days=year)
            #format our str with our date_format
            formatted_dates = datetime.strftime(dates, date_format)
            #create query which will iterate through desired weather period
            query = 'http://api.wunderground.com/api/'+ api +'/history_'+formatted_dates+'/q/'+state+'/'+city+'.json'
            #iterate through the number of days and query the api. dump json results every time 
            f = urllib2.urlopen(query)
            #read query as a json string
            json_string = f.read()
            #parse/load json string
            parsed_json = json.loads(json_string)
            #Iterate through each json object and append it to an ordered dictionary
            for i in parsed_json['history']['observations']:        
                d = collections.OrderedDict()
                d['date'] = i['date']['mon'] + '/' + i['date']['mday'] + '/' + i['date']['year']
                d['time'] = i['date']['pretty'][0:8]
                d['temp'] = i['tempi']
                d['conds'] = i['conds']
                d['wdire'] = i['wdire']
                d['wdird'] = i['wdird']
                d['hail'] = i['hail']
                d['thunder'] = i['thunder']
                d['pressurei'] = i['pressurei']
                d['snow'] = i['snow']
                d['pressurem'] = i['pressurem']
                d['fog'] = i['fog']
                d['tornado'] = i['tornado']
                d['hum'] = i['hum']
                d['tempi'] = i['tempi']
                d['tempm'] = i['tempm']
                d['dewptm'] = i['dewptm']
                d['dewpti'] = i['dewpti']
                d['rain'] = i['rain']
                d['visim'] = i['visi']
                d['wspdi'] = i['wspdi']
                d['wspdm'] = i['wspdm']
                objects_list.append(d)
                #dump the dictionary into a json object
                j = json.dumps(objects_list)
        #append our json object to a list for every day and return its data
    #    print j
        return j
    #If we just need the data for ONE day (pass None for end_date):
    if(end_date is None):
        f = urllib2.urlopen('http://api.wunderground.com/api/API_KEY/history_'+start_date+'/q/'+state+'/'+city+'.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
    
        objects_list = []
        for i in parsed_json['history']['observations']:        
            d = collections.OrderedDict()
            d['date'] = i['date']['mon'] + '/' + i['date']['mday'] + '/' + i['date']['year']
            d['time'] = i['date']['pretty'][0:8]
            d['temp'] = i['tempi']
            d['conds'] = i['conds']
            d['wdire'] = i['wdire']
            d['wdird'] = i['wdird']
            d['hail'] = i['hail']
            d['thunder'] = i['thunder']
            d['pressurei'] = i['pressurei']
            d['snow'] = i['snow']
            d['pressurem'] = i['pressurem']
            d['fog'] = i['fog']
            d['tornado'] = i['tornado']
            d['hum'] = i['hum']
            d['tempi'] = i['tempi']
            d['tempm'] = i['tempm']
            d['dewptm'] = i['dewptm']
            d['dewpti'] = i['dewpti']
            d['rain'] = i['rain']
            d['visim'] = i['visi']
            d['wspdi'] = i['wspdi']
            d['wspdm'] = i['wspdm']
            objects_list.append(d)
        
        j = json.dumps(objects_list)
        return j

query_results = get_weather_data('API_KEY','Austin','TX', '20130101', '20130131')

df = pd.read_json(query_results)



```
__________
##January
![alt text](month_temp_graphs/January_Weather.png "")
##April
![alt text](month_temp_graphs/April_Weather.png "")
##July
![alt text](month_temp_graphs/July_Weather.png "")
##October
![alt text](month_temp_graphs/October_Weather.png "")

