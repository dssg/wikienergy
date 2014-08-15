from disaggregator import GreenButtonDatasetAdapter as gbda
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

def run_regressions(trace_series,temps_series,cal_hdd_temp_range=range(50,60),
        cal_cdd_temp_range=range(60,75),plot=False):
    '''
    Takes in a series from a trace and a temperature series and runs linear regressions
    over a range of cooling and heating setpoints. For each linear regression, temperature
    values above the setpoint are used, with temps below the cooling setpoint (and above
    the heating setpoint) are set to the setpoint. This is to make the linear regression
    similar to those conducted for cooling and heating degree days.  This method outputs
    a dictionary containing the best slopes and intercepts, as well as their corresponding
    setpoint temperatures and adjusted r2 values.
    '''
    results_dict = {}
    df_trace = pd.DataFrame(trace_series,columns=['kwh'])
    df_trace = df_trace.sort_index()
    best_r2_adj_cool = float("-inf")
    best_r2_adj_heat = float("-inf")
    best_cdd_temp = 0
    best_hdd_temp = 0
    slope_cdd = None
    slope_hdd = None
    intercept_hdd = None
    intercept_cdd = None
    results_cdd = None
    results_hdd = None
    df_all_best_cool = None
    df_all_best_heat = None

    df_temps=pd.DataFrame(temps_series,columns=['temp'])

    for cdd_setpoint in cal_cdd_temp_range:
        df_temps_dropped=df_temps.drop(df_temps[df_temps['temp']<=cdd_setpoint].index)
        df_all = pd.merge(df_trace,df_temps_dropped,left_index=True,right_index=True)
        if(len(df_all) > 1):
            results = pd.ols(y=df_all['kwh'], x = df_all['temp'])
            r2_adj = results.r2_adj
            if(r2_adj > best_r2_adj_cool):
                best_cdd_temp = cdd_setpoint
                best_r2_adj_cool = r2_adj
                slope_cdd = results.beta[0]
                intercept_cdd = results.beta[1]
                results_cdd=results
                df_all_best_cool = df_all
    if plot and df_all_best_cool is not None and len(df_all_best_cool) > 1:
        df_plot=df_all_best_cool.drop(df_all_best_cool[df_all_best_cool['temp']==best_cdd_temp].index)
        plt.plot(df_plot['temp'],df_plot['kwh'],'.r')
        x = np.arange(best_cdd_temp,100,.2)
        y = x * slope_cdd + intercept_cdd
        plt.plot(x,y,'k')

    for hdd_setpoint in cal_hdd_temp_range:
        df_temps_dropped=df_temps.drop(df_temps[df_temps['temp']>=hdd_setpoint].index)
        df_all = pd.merge(df_trace,df_temps_dropped,left_index=True,right_index=True)
        if(len(df_all) > 1):
            results = pd.ols(y=df_all['kwh'], x=df_all['temp'])
            r2_adj = results.r2_adj
            if(r2_adj > best_r2_adj_heat):
                best_hdd_temp = hdd_setpoint
                best_r2_adj_heat = r2_adj
                slope_hdd = results.beta[0]
                intercept_hdd = results.beta[1]
                results_hdd=results
                df_all_best_heat = df_all

    if plot and df_all_best_heat is not None and len(df_all_best_heat) > 1:
        df_plot=df_all_best_heat.drop(df_all_best_heat[df_all_best_heat['temp']==best_hdd_temp].index)
        plt.plot(df_plot['temp'],df_plot['kwh'],'.')
        x = np.arange(10,best_hdd_temp,.2)
        y = x*slope_hdd + intercept_hdd
        plt.plot(x,y,'k')

    results_dict['slope_hdd'] = slope_hdd
    results_dict['intercept_hdd'] = intercept_hdd
    results_dict['best_hdd_temp'] = best_hdd_temp
    results_dict['best_r2_adj_hdd'] = best_r2_adj_heat
    results_dict['slope_cdd'] = slope_cdd
    results_dict['intercept_cdd'] = intercept_cdd
    results_dict['best_cdd_temp'] = best_cdd_temp
    results_dict['best_r2_adj_cdd'] = best_r2_adj_cool
    results_dict['results_cdd'] = results_cdd
    results_dict['results_hdd'] = results_hdd
    return results_dict


def run_regressions_and_predict(trace_series,temps_series,
        cal_heat_temp_range=range(50,60),cal_cool_temp_range=range(60,75),
        plot=False,json=False):
    '''
    A wrapper method that both runs the run_regressions and predict_from_regressions
    methods. It returns the actual total energy value (trace_series), the HVAC
    disaggregated signal, and the difference between the actual total energy value
    and the disaggregated TOTAL signal (based on our linear regression). This
    output can be in json format if the json parameter is set to true, otherwise
    it outputs as a triple.
    '''
    results_dict = run_regressions(trace_series,temps_series,
        cal_heat_temp_range,cal_cool_temp_range,plot)
    [total_series,air_series,diff_series] = predict_from_regressions(trace_series,
            temps_series,results_dict)
    if(json):
        json_string=get_results_to_json(total_series,air_series,diff_series,
                results_dict['slope_cdd'])
        return json_string
    else:
        return [total_series,air_series,diff_series]

def get_results_to_json(total_series,air_series,diff_series,slope_cdd):
    '''
    This method takes in a triple of series and puts them into json format
    for use on the website.
    '''

    perc_correlation=len([val for val in diff_series if abs(val) < 5000])\
        /float(len(diff_series))*100

    data=[]
    json_object={}
    json_object['perc_correlation'] = perc_correlation
    json_object['slope_cdd'] = slope_cdd
    json_object['min_diff'] = min(diff_series/1000)
    json_object['max_diff'] = max(diff_series/1000)
    for i, v in total_series.iteritems():
        kwh = v/1000
        air = air_series[i]/1000
        diff=diff_series[i]/1000
        data.append({'date':i.strftime('%Y-%m-%d %H:%M'),
            'reading': float(kwh),'air_reading':float(air),
            'diff_reading':float(diff)})
    json_object['data']=data
    json_string = json.dumps(json_object, ensure_ascii=False,
                             indent=4, separators=(',', ': '))

    return json_string

def predict_from_regressions(trace_series,temps_series,results_dict):
    '''
    Takes a series of a trace and of temperature, as well as the dictionary
    output by the run_regression method, and outputs a prediction of the total
    energy usage, and subsequent HVAC usage. It returns the actual total energy
    value (trace_series), the HVAC disaggregated signal, and the difference
    between the actual total energy value and the disaggregated TOTAL signal
    (based on our linear regression).
    '''
    slope_hdd = results_dict['slope_hdd']
    intercept_hdd = results_dict['intercept_hdd']
    best_hdd_temp = results_dict['best_hdd_temp']

    slope_cdd = results_dict['slope_cdd']
    intercept_cdd = results_dict['intercept_cdd']
    best_cdd_temp = results_dict['best_cdd_temp']

    df_trace = pd.DataFrame(trace_series,columns=['kwh'])
    df_trace = df_trace.sort_index()
    df_trace = df_trace
    df_temps = pd.DataFrame(temps_series,columns=['temp'])
    df_sub = pd.merge(df_trace,df_temps,left_index=True,right_index=True)

    pred_air_daily = []
    total_daily = []
    pred_total_daily = []
    if(intercept_cdd):
        intercept_cdd_new = best_cdd_temp*slope_cdd+intercept_cdd
    if(intercept_hdd):
        intercept_hdd_new = best_hdd_temp*slope_hdd+intercept_hdd

    for i,val in enumerate(df_sub['kwh']):
        use_kwh_per_day = float(val)
        if df_sub['temp'][i] > best_cdd_temp:
            pred_air_kwh_per_day = df_sub['temp'][i]*slope_cdd+intercept_cdd-intercept_cdd_new
            pred_total_kwh_per_day = df_sub['temp'][i]*slope_cdd+intercept_cdd
        elif df_sub['temp'][i] < best_hdd_temp:
            pred_air_kwh_per_day = df_sub['temp'][i]*slope_hdd+intercept_hdd-intercept_hdd_new
            pred_total_kwh_per_day = df_sub['temp'][i]*slope_hdd+intercept_hdd
        pred_total_daily.append(pred_total_kwh_per_day)
        if pred_air_kwh_per_day > use_kwh_per_day:
            pred_air_kwh_per_day = use_kwh_per_day
        pred_air_daily.append(pred_air_kwh_per_day)
        total_daily.append(use_kwh_per_day)

    total_series = pd.Series(total_daily,index=df_sub['kwh'].index)
    air_series = pd.Series(pred_air_daily,index=df_sub['kwh'].index)
    diff_daily = np.array(total_daily)-np.array(pred_total_daily)
    diff_series = pd.Series(diff_daily,index=df_sub['kwh'].index)

    return [total_series,air_series,diff_series]

def get_sensitivity_to_json(diff_series,slope_cdd):
    perc_correlation=len([val for val in diff_series if abs(val) < 5000])\
        /float(len(diff_series))*100

    data.append({'sureness':float(perc_correlation),
        'sensitivity': slope_cdd})

    json_string = json.dumps(data, ensure_ascii=False,
                         indent=4, separators=(',', ': '))

    return json_string
