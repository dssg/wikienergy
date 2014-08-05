"""
.. module:: weather
   :platform: Unix
   :synopsis: Contains utilities for obtaining weather data and performing
      temperature normalization. Also includes utilities for converting
      temperatures to heating/cooling degree days.

.. moduleauthor:: Phil Ngo <ngo.phil@gmail.com>
.. moduleauthor:: Miguel Perez <miguel@invalid.com>
.. moduleauthor:: Stephen Suffian <steve@invalid.com>
.. moduleauthor:: Sabina Tomkins <sabina@invalid.com>

"""
import urllib2
import json
from datetime import datetime, timedelta, date
import collections
import pandas as pd


def degree_day_regression(df, x_opt='both'):
    '''
    Function that runs the weather normalization regression on energy use data
    --------------
    df: dataframe that includes
        use per day (upd)
        heating degree days per day (hddpd)
        cooling degree days per day (cddpd)
    ---------------
    x_opt: options for the regression function
        'hdd': run regression with just heating degree days
        'cdd': run regression with just cooling degree days
        'both' (default):
    '''

    if x_opt == 'hdd':
        covar = {'HDD': df.hdd_per_day}
        results = pd.ols(y=df.use_per_day, x = covar)
        return pd.DataFrame([[results.beta[1], results.std_err[1],
                              results.beta[0], results.std_err[0],
                              results.r2, results.r2_adj, results.nobs ]],
                            columns = ['intercept', 'intercept_std_err',
                                       'HDD', 'HDD_std_err',
                                       'R2', 'R2_adj','N_reads'])
    elif x_opt == 'cdd':
        covar = {'CDD': df.cdd_per_day}
        results = pd.ols(y=df.use_per_day, x = covar)
        return pd.DataFrame([[results.beta[1], results.std_err[1],
                              results.beta[0], results.std_err[0],
                              results.r2, results.r2_adj, results.nobs]],
                              columns = ['intercept', 'intercept_std_err',
                                         'CDD', 'CDD_std_err',
                                         'R2', 'R2_adj','N_reads'])
    elif x_opt == 'both':
        covar = {'CDD': df.cdd_per_day, 'HDD': df.hdd_per_day}
        results = pd.ols(y=df.use_per_day, x = covar)
        return pd.DataFrame([[results.beta[2], results.std_err[2],
                              results.beta[0], results.std_err[0],
                              results.beta[1], results.std_err[1],
                              results.r2, results.r2_adj, results.nobs]],
                            columns = ['intercept', 'intercept_std_err',
                                       'CDD', 'CDD_std_err',
                                       'HDD','HDD_std_err',
                                       'R2', 'R2_adj','N_reads'])
def get_hdd(ref_temp,df):
    '''
    Converts a temperature to HDD.
    '''
    df['hdd']=ref_temp-df.temps
    df['hdd'].loc[df.hdd<0]=0
    df['hdd_cum']=df.hdd.cumsum()
    return df

def get_cdd(ref_temp,df):
    '''
    Converts a temperature to HDD.
    '''
    df['cdd']=df.temps-ref_temp
    df['cdd'].loc[df.cdd<0]=0
    df['cdd_cum']=df.cdd.cumsum()
    return df

def get_weather_data_as_df(api,city,state,start_date,end_date):
    """
    Return a dataframe indexed by time containing hourly weather data
    """
    query_results=get_weather_data(api,city,state,start_date,end_date)
    temp_temps=pd.read_json(query_results)
    return _combine_date_time_and_index(temp_temps)

def get_weather_data(api,city,state,start_date,end_date):
    '''
    Returns a json string given a city, state, and desired date (YYYYMMDD)
    '''
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

def weather_normalize(trace,temperature,set_point):
    '''
    Returns a weather-normalized trace
    '''
    pass

def _index_df_by_date(df):
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.index.snap() # snap to nearest frequency

def _combine_date_time_and_index(temp_df):
    for i,date in enumerate(temp_df['date']):
        hour_min=temp_df['time'][i].split(':')
        hour=hour_min[0]
        min_ampm=hour_min[1].split(' ')
        minute=min_ampm[0]
        if('PM' in min_ampm[1]):
            hour=int(hour)+12
            if(hour is 24):
                hour=0
        temp_df['date'][i]=date.replace(hour=int(hour),minute=int(minute))
    _index_df_by_date(temp_df)
    return temp_df

