import json
import urllib2
from calendar import monthrange
import datetime

def get_solar_data_from_nrel(api,zip_code):
    f = urllib2.urlopen('http://developer.nrel.gov/api/solar/solar_resource/'
           +'v1.json?api_key='+api+'&address='+zip_code)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    return parsed_json['outputs']['avg_lat_tilt']['monthly']

months = ['jan', 'feb' , 'mar', 'apr', 'may', 'jun',
            'jul','aug' 'sep','oct','nov','dec']

def get_month_solar_data(month_num,month_data):
    for i in range(1, 13)):
        if month_num is i:
            return month_data[months[i]]
    else:
        raise ValueError("invalid month number.")    

def calculate_solar_generated(start_dt,end_dt,pv_size,api,zip_code,eff_factor=0.8):

    month_data=get_solar_data_from_nrel(api,zip_code)
    delta = end_dt - start_dt

    this_month = start_dt.month
    total_kWh = 0
    for val in range(delta.days+1):
        delta_days=datetime.timedelta(val)
        total_kWh = total_kWh + get_month_solar_data(this_month,
                month_data)*pv_size*eff_factor
        if (start_dt+delta_days).month is not this_month:
            this_month=(start_dt+delta_days).month

    data = []
    kwh = v/1000
    data.append({'solar_savings':total_kWh/float(1000)})
    json_string = json.dumps(data, ensure_ascii=False)
    return json_string

