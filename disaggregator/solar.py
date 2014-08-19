import json
import urllib2
from calendar import monthrange
import datetime

def get_solar_data_from_nrel(api,zip_code):
    f = urllib2.urlopen('http://developer.nrel.gov/api/solar/solar_resource/'
           +'v1.json?api_key='+str(api)+'&address='+str(zip_code))
    json_string = f.read()
    parsed_json = json.loads(json_string)
    return parsed_json['outputs']['avg_lat_tilt']['monthly']


def get_month_solar_data(month_num,month_data):
    months = ['jan', 'feb' , 'mar', 'apr', 'may', 'jun',
            'jul','aug' 'sep','oct','nov','dec']
    for i in range(1, 13):
        if month_num is i:
            return month_data[months[i]]


def calculate_solar_generated(start_dt,end_dt,api,zip_code,month_data,eff_factor=0.8):

    month_data = get_solar_data_from_nrel(api,zip_code)
    delta = end_dt - start_dt
    data = []
    this_month = start_dt.month
    total_kWh = 0
    for val in range(delta.days+1):
        delta_days=datetime.timedelta(val)
        month_name= get_month_name(this_month)
        total_kWh=total_kWh+month_data[month_name]*eff_factor
        if (start_dt+delta_days).month is not this_month:
            data.append({'date':str(month_name.title())+' ' + str((start_dt+delta_days).year) ,'value':total_kWh/float(1000)})
            this_month=(start_dt+delta_days).month

    json_string = json.dumps(data, ensure_ascii=False)
    return json_string
