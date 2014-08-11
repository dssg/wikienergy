from disaggregator import GreenButtonDatasetAdapter as gbda
import pandas as pd
import numpy as np
import json

def get_temperatures(date_start,date_end):
    import pickle
    with open('temp_oakpark_20120101_20140730.pkl','rb') as f:
        oak_park_temps_df=pickle.load(f)
    oak_park_temps = pd.Series(oak_park_temps_df['temp'],index=oak_park_temps_df.index)
    oak_park_temps = oak_park_temps.resample('24H', fill_method='ffill')
    oak_park_temps = oak_park_temps
    outlier_thresh = np.mean(oak_park_temps)-(5*np.std(oak_park_temps))
    oak_park_temps = remove_low_outliers(oak_park_temps,outlier_thresh,24)
    return oak_park_temps

def remove_low_outliers(series,threshold,num_hours):
    outliers=series[series < threshold].index
    a=0
    for a,i in enumerate(outliers):
        try: series[i]=series[i-pd.DateOffset(hours=num_hours)]
        except KeyError: series[i]= series[i+pd.DateOffset(hours=num_hours)]
    return series

def run_regressions(trace,temps,cal_hdd_temp_range,cal_cdd_temp_range):
    results_dict={}
    df_trace=pd.DataFrame(trace.series,columns=['kwh'])
    df_trace=df_trace.sort_index()
    df_temps=pd.DataFrame(temps,columns=['temp'])

    best_r2_adj_cool=float("-inf")
    best_r2_adj_heat=float("-inf")
    best_cdd_temp=0
    best_hdd_temp=0
    slope_cdd=None
    slope_hdd=None
    intercept_hdd=None
    intercept_cdd=None
    df_all_best=None

    for cdd_setpoint in cal_cdd_temp_range:
        df_temps_dropped=df_temps.drop(df_temps[df_temps['temp']<=cdd_setpoint].index)
        df_all=pd.merge(df_trace,df_temps_dropped,left_index=True,right_index=True)
        if(len(df_all)>0):
            results = pd.ols(y=df_all['kwh'], x = df_all['temp'])
            r2_adj=results.r2_adj
            if(r2_adj>best_r2_adj_cool):
                best_cdd_temp=cdd_setpoint
                best_r2_adj_cool=r2_adj
                slope_cdd=results.beta[0]
                intercept_cdd=results.beta[1]
                df_all_best=df_all

    for hdd_setpoint in cal_hdd_temp_range:
        df_temps_dropped=df_temps.drop(df_temps[df_temps['temp']>=hdd_setpoint].index)
        df_all=pd.merge(df_trace,df_temps_dropped,left_index=True,right_index=True)
        if(len(df_all)>0):
            results = pd.ols(y=df_all['kwh'], x = df_all['temp'])
            r2_adj=results.r2_adj
            if(r2_adj>best_r2_adj_heat):
                best_hdd_temp=hdd_setpoint
                best_r2_adj_heat=r2_adj
                slope_hdd=results.beta[0]
                intercept_hdd=results.beta[1]
                df_all_best=df_all

    results_dict['slope_hdd']=slope_hdd
    results_dict['intercept_hdd']=intercept_hdd
    results_dict['best_hdd_temp']=best_hdd_temp
    results_dict['best_r2_adj_hdd']=best_r2_adj_heat
    results_dict['slope_cdd']=slope_cdd
    results_dict['intercept_cdd']=intercept_cdd
    results_dict['best_cdd_temp']=best_cdd_temp
    results_dict['best_r2_adj_cdd']=best_r2_adj_cool
    return results_dict

def open_xml_and_run_regression(filepath,cal_heat_temp_range=range(50,60),cal_cool_temp_range=range(60,70)):
    with open(filepath,'rb') as f:
        xml_house=f.read()
    trace=gbda.get_trace(xml_house)
    trace = trace.resample('24H',method='sum')
    trace.series = remove_low_outliers(trace.series,0,24)

    date_start = trace.series.index[0]
    date_end = trace.series.index[len(trace.series)-1]
    temps_series = get_temperatures(date_start,date_end)

    results_dict=run_regressions(trace,temps_series,
        cal_heat_temp_range,cal_cool_temp_range)
    return [trace, temps_series, results_dict]

def predict_from_results(trace,temps,results_dict):
    slope_hdd = results_dict['slope_hdd']
    intercept_hdd = results_dict['intercept_hdd']
    best_hdd_temp = results_dict['best_hdd_temp']

    slope_cdd = results_dict['slope_cdd']
    intercept_cdd = results_dict['intercept_cdd']
    best_cdd_temp = results_dict['best_cdd_temp']

    df_trace = pd.DataFrame(trace.series,columns=['kwh'])
    df_trace = df_trace.sort_index()
    df_trace = df_trace
    df_temps = pd.DataFrame(temps,columns=['temp'])
    df_sub = pd.merge(df_trace,df_temps,left_index=True,right_index=True)

    pred_air_daily=[]
    total_daily=[]
    pred_total_daily=[]

    intercept_cdd_new=best_cdd_temp*slope_cdd+intercept_cdd
    intercept_hdd_new=best_hdd_temp*slope_hdd+intercept_hdd

    for i,val in enumerate(df_sub['kwh']):
        use_kwh_per_day=float(val)
        if(df_sub['temp'][i]>best_cdd_temp):
            pred_air_kwh_per_day=df_sub['temp'][i]*slope_cdd+intercept_cdd-intercept_cdd_new
            pred_total_kwh_per_day=df_sub['temp'][i]*slope_cdd+intercept_cdd
        elif(df_sub['temp'][i]<best_hdd_temp):
            pred_air_kwh_per_day=df_sub['temp'][i]*slope_hdd+intercept_hdd-intercept_hdd_new
            pred_total_kwh_per_day=df_sub['temp'][i]*slope_hdd+intercept_hdd
        pred_total_daily.append(pred_total_kwh_per_day)
        if(pred_air_kwh_per_day>use_kwh_per_day):
            pred_air_kwh_per_day=use_kwh_per_day
        pred_air_daily.append(pred_air_kwh_per_day)
        total_daily.append(use_kwh_per_day)

    total_series=pd.Series(total_daily,index=df_sub['kwh'].index)
    air_series=pd.Series(pred_air_daily,index=df_sub['kwh'].index)
    diff_daily=np.array(total_daily)-np.array(pred_total_daily)
    diff_series=pd.Series(diff_daily,index=df_sub['kwh'].index)

    return [total_series,air_series,diff_series]

def open_xml_and_get_results(filepath):
    [trace,temps_series,results_dict] = open_xml_and_run_regression(filepath)
    [total_series,air_series,diff_series] = predict_from_results(trace,temps_series,results_dict)
    data=[]
    for i, v in total_series.iteritems():
        kwh = v/1000
        data.append({'date':i.strftime('%Y-%m-%d %H:%M'),
            'reading': float(kwh),'air_reading':air_series[i],
            'diff_series':diff_series[i]})
    json_string = json.dumps(data, ensure_ascii=False,
                             indent=4, separators=(',', ': '))

    return json_string

