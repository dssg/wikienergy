"""
.. module:: disaggregator.utils
   :platform: Unix
   :synopsis: Contains utility methods for modifying and converting between
      appliance classes.

.. moduleauthor:: Phil Ngo <ngo.phil@gmail.com>
.. moduleauthor:: Stephen Suffian <steve@invalid.com>

"""



import appliance
import pandas as pd
import numpy as np
import os
import pickle
import sys


def aggregate_instances(instances, metadata, how="strict"):
    '''
    Given a list of temporally aligned instances, aggregate them into a single
    signal.
    '''
    if how == "strict":
        traces = [instance.traces for instance in instances]
        traces = [list(t) for t in zip(*traces)] # transpose
        traces = [ aggregate_traces(t,{}) for t in traces]
        return appliance.ApplianceInstance(traces, metadata)
    else:
        return NotImplementedError

def aggregate_traces(traces, metadata, how="strict"):
    '''
    Given a list of temporally aligned traces, aggregate them into a single
    signal.
    '''
    if how == "strict":
        # require that traces are exactly aligned
        summed_series = traces[0].series
        for trace in traces[1:]:
            summed_series += trace.series
        return appliance.ApplianceTrace(summed_series, metadata)
    else:
        return NotImplementedError

def get_common_ids(id_lists):
    '''
    Returns a list of ids common to the supplied lists. (id set intersection)
    '''
    id_sets = [set(id_list) for id_list in id_lists]
    common_ids = id_sets[0]
    for id_set in id_sets[1:]:
        common_ids &= id_set
    return list(common_ids)


def split_trace_into_daily(trace):
    '''
    Given a single trace, a list of traces are returned that are each
    from a unique date.
    '''
    series_list=None;
    traces=[]
    for i,group in enumerate(trace.series.groupby(trace.series.index.date)):
            metadata=trace.metadata
            metadata['trace_num']=i
            traces.append(appliance.ApplianceTrace(group[1],metadata))
    return traces

def split_instance_traces_into_daily(device_instance):
    '''
    Each trace in an instance is split into multiple traces that are each
    from a unique date
    '''
    traces=[]
    for trace in instance.traces:
        traces.extend(split_trace_into_daily(trace))
    device_instance.traces=traces
    return device_instance

def split_type_traces_into_daily(device_type):
    '''
    Each trace in each instance of a type is split into multiple traces 
    that are each from a unique date
    '''
    traces=[]
    instances=[]
    for instance in device_type.instances:
        for trace in instance.traces:
            traces.extend(split_trace_into_daily(trace))
        instance.traces=traces
        instances.append(instance)
    device_type.instances=instances    
    return device_type

def concatenate_traces(traces, metadata=None, how="strict"):
    '''
    Given a list of appliance traces, returns a single concatenated
    trace. With how="strict" option, must be sampled at the same rate and
    consecutive, without overlapping datapoints.
    '''
    if not metadata:
        metadata = traces[0].metadata

    if how == "strict":
        # require ordered list of consecutive, similarly sampled traces with no
        # missing data.
        return appliance.ApplianceTrace(pd.concat([t.series for t in traces]),metadata)
    else:
        raise NotImplementedError

def concatenate_traces_lists(traces, metadata=None, how="strict"):
    '''
    Takes a list of lists of n traces and concatenates them into a single
    list of n traces.
    '''
    if not metadata:
        metadata = [trace.metadata for trace in traces[0]]

    if how == "strict":
        traces = [list(t) for t in zip(*traces)]
        traces = [concatenate_traces(t,m) for t,m in zip(traces,metadata)]
        return traces
    else:
        raise NotImplementedError

def order_traces(traces):
    '''
    Given a set of traces, orders them chronologically and catches
    overlapping traces.
    '''
    order = np.argsort([t.series[0] for t in traces])
    new_traces = [traces[i] for i in order]
    return new_traces

def pickle_object(obj,title):
    '''
    Given an object and a filename saves the object in pickled format to the data directory.
    '''

    #sys.path.append('../../')
    silly_path = os.path.abspath(os.path.join(os.path.dirname( '' ), '../..','data/'))
    with open(os.path.join(silly_path,'{}.p'.format(title)),'wb') as f:
        pickle.dump(object, f)

def shuffle_appliance_sets(sets,other_params):
    pass


