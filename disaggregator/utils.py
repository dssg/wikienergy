"""
.. module:: utils
   :platform: Unix
   :synopsis: Contains utility methods for modifying and converting between
      appliance classes.

.. moduleauthor:: Phil Ngo <ngo.phil@gmail.com>
.. moduleauthor:: Miguel Perez <miguel@invalid.com>
.. moduleauthor:: Stephen Suffian <steve@invalid.com>
.. moduleauthor:: Sabina Tomkins <sabina@invalid.com>

"""



import appliance
import pandas as pd
import numpy as np
import os
import pickle
import sys
import decimal
import datetime
import random
import copy


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

def bootstrap_appliance_set(appliance_sets, k, n, how="strict"):
    """
    Returns a list of n bootstrapped appliance sets (each with k appliances).
    Fails if how="strict" and appliance sets are not aligned.
    """
    # TODO write this function.
    pass

def create_datetimeindex(df):
    """
    Modify a dataframe inplace to give it a DatetimeIndex. Must have the column
    'time', which will be removed and used as the index.
    """
    no_tz = [t.replace(tzinfo=None) for t in df['time']] # is this efficient?
    df['time'] = pd.to_datetime(no_tz,utc=True)
    df.set_index('time', inplace=True)
    df.index.snap() # snap to nearest frequency


def get_common_ids(id_lists):
    '''
    Returns a list of ids common to the supplied lists. (id set intersection)
    '''
    id_sets = [set(id_list) for id_list in id_lists]
    common_ids = id_sets[0]
    for id_set in id_sets[1:]:
        common_ids &= id_set
    return sorted(list(common_ids))


def get_train_valid_test_indices(n):
    '''
    Given an number n, return three arrays of length n/2, n/4, n/4 respectively,
    which collectively contain the indices [0..n-1] ordered psuedo-randomly.
    '''
    indices = np.arange(n)
    np.random.shuffle(indices)
    n_train = n/2
    n_valid = n/4
    n_test = n - n_train - n_valid
    assert(n == n_train + n_valid + n_test)
    return (sorted(indices[:n_train]),
            sorted(indices[n_train:n_train+n_valid]),
            sorted(indices[n_train+n_valid:]))

def split_trace_into_rate(trace,rate):
    '''
    Given a single trace, a list of traces are returned that are each
    from a unique date.
    '''
    print "WARNING: deprecated, "\
          "use appliance trace.split_into_rate(rate) instead"
    # set rate to group by
    if rate == 'D' or rate == '1D':
        groupby_rate = trace.series.index.date
    elif rate == 'W' or rate == '1W':
        groupby_rate = trace.series.index.week
    else:
        raise NotImplementedError('Looking for "week" or "day"')

    traces=[]
    for i, group in enumerate(trace.series.groupby(groupby_rate)):
        metadata = dict.copy(trace.metadata)
        metadata['trace_num'] = i
        traces.append(appliance.ApplianceTrace(group[1],metadata))
    return traces

def split_instance_traces_into_rate(device_instance,rate):
    '''
    Each trace in an instance is split into multiple traces that are each
    from a unique date
    '''
    print "WARNING: deprecated, "\
          "use appliance_instance.split_by(rate) instead"
    traces=[]
    for trace in device_instance.traces:
        traces.extend(split_trace_into_rate(trace,rate))
    return appliance.ApplianceInstance(traces,device_instance.metadata)

def split_type_traces_into_rate(device_type, rate):
    '''
    Each trace in each instance of a type is split into multiple traces
    that are each from a unique date
    '''
    print "WARNING: deprecated, "\
          "use appliance_type.split_by(rate) instead"
    instances=[]
    for instance in device_type.instances:
        new_instance= split_instance_traces_into_rate(instance,rate)
        instances.append(new_instance)
    return appliance.ApplianceType(instances,device_type.metadata)

def split_set_traces_into_rate(device_set, rate):
    '''
    Each trace in each instance of a set is split into multiple traces
    that are each from a unique date
    '''
    print "WARNING: deprecated, "\
          "use appliance_set.split_by(rate) instead"
    instances=[]
    for instance in device_set.instances:
        new_instance= split_instance_traces_into_rate(instance,rate)
        instances.append(new_instance)
    return appliance.ApplianceSet(instances,device_set.metadata)

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
        return appliance.ApplianceTrace(pd.concat([t.series for t in traces]),
                                        metadata)
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

def resample_trace(trace,sample_rate):
    '''
    Takes a trace and resamples it to a given sample rate, defined by the
    offset aliases described in panda time series.
    http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
    '''
    print "WARNING: deprecated, "\
          "use appliance_trace.resample(sample_rate) instead"
    try:
        new_series=trace.series.astype(float)
        new_series=new_series.resample(sample_rate,how='mean')
        new_series=new_series.map(decimal.Decimal)
        new_series.name=trace.series.name
        return appliance.ApplianceTrace(new_series,trace.metadata)
    except ValueError:
        raise SampleError(self.sample_rate)


def resample_instance_traces(device_instance,sample_rate):
    '''
    Resamples all traces within a given instance.
    '''
    print "WARNING: deprecated, "\
          "use appliance_instance.resample(sample_rate) instead"
    new_traces=[]
    for trace in device_instance.traces:
        new_traces.append(resample_trace(trace,sample_rate))
    return appliance.ApplianceInstance(new_traces,device_instance.metadata)

def resample_type_traces(device_type,sample_rate):
    '''
    Resamples all traces in each instance of a given type.
    '''
    print "WARNING: deprecated, "\
          "use appliance_type.resample(sample_rate) instead"
    new_instances=[]
    for instance in device_type.instances:
        new_instances.append(resample_instance_traces(instance,sample_rate))
    return appliance.ApplianceType(new_instances,device_type.metadata)

def resample_set_traces(device_set,sample_rate):
    '''
    Resamples all traces in each instance of a given type.
    '''
    new_instances=[]
    for instance in device_set.instances:
        new_instances.append(resample_instance_traces(instance,sample_rate))
    return appliance.ApplianceSet(new_instances,device_set.metadata)

def order_traces(traces):
    '''
    Given a set of traces, orders them chronologically and catches
    overlapping traces.
    '''
    order = np.argsort([t.series.index[0] for t in traces])
    new_traces = [traces[i] for i in order]
    return new_traces

def pickle_object(obj,title):
    '''
    Given an object and a filename saves the object in pickled format to the data directory.
    '''
    
    current_path = os.getcwd()
    rel = os.path.relpath(os.path.join(current_path.split('wikienergy')[0],'wikienergy'),current_path)
    path = os.path.abspath(os.path.join(os.getcwd(),rel))
    file = os.path.join(os.path.abspath(os.path.join(os.getcwd(),rel)),'data/{}.p'.format(title))
#print open(os.path.join(rel_path,'{}.p'.format(title)),'wb')

    with open(file,'wb') as f:
        pickle.dump(obj, f)


def generate_random_appliance_sets(appliance_sets,k,n):
    """
    Given a list of appliance sets, returns n randomly
    sets, whose instances have been sampled
    (w/replacement) from the instances of the given appliance_sets.

    ApplianceSets must be aligned.
    """
    all_instances = [instance for appliance_set in appliance_sets
                     for instance in appliance_set.instances]
    n_instances = len(all_instances)
    all_sets = []
    for _ in xrange(n):
        instances = []
        for _ in xrange(k):
            instance = all_instances[random.randrange(n_instances)]
            instances.append(instance)
        metadata = {'name': None, 'source': "random sample"}
        appliance_set = appliance.ApplianceSet(instances, metadata)
        all_sets.append(appliance_set)
    return all_sets


def trace_series_to_numpy_array(values):
    '''
    This takes the series from a trace and converts it to a numpy array for
    ingestion into HMMs and certain plots. It also removes the NaNs.
    '''
    a=[]
    X=[]
    for i in values:
        a.append(float(i))
        X.append(a)
        a=[]
    array=np.array(X)
    whereAreNaNs = np.isnan(array);
    array[whereAreNaNs] = 0;
    return array

def get_trace_in_time_of_day(device_trace,start_time,end_time):
    '''
    Given a trace and a start and end datetime.time, it returns a trace
    within that time period.
    '''
    print "WARNING: deprecated, "\
          "use trace.get_time_of_day(start_time,end_time) instead"
    new_series=device_trace.series.ix[start_time:end_time]
    return appliance.ApplianceTrace(new_series,device_trace.metadata)

def get_instance_in_time_of_day(device_instance,start_time,end_time):
    '''
    Given an instance and a start and end datetime.time, it returns a trace within that time period.
    '''
    print "WARNING: deprecated, "\
          "use instance.get_time_of_day(start_time,end_time) instead"
    new_traces=[]
    for trace in device_instance.traces:
        new_traces.append(get_trace_in_time_of_day(trace,start_time,end_time))
    return appliance.ApplianceInstance(new_traces,device_instance.metadata)

def get_type_in_time_of_day(device_type,start_time,end_time):
    '''
    Resamples all traces in each instance of a given type.
    '''
    print "WARNING: deprecated, "\
          "use type.get_time_of_day(start_time,end_time) instead"
    new_instances=[]
    for instance in device_type.instances:
        new_instances.append(get_instance_in_time_of_day(instance,start_time,end_time))
    return appliance.ApplianceType(new_instances,device_type.metadata)

def get_set_in_time_of_day(device_set,start_time,end_time):
    '''
    Resamples all traces in each instance of a given set.
    '''
    print "WARNING: deprecated, "\
          "use set.get_time_of_day(start_time,end_time) instead"
    new_instances = []
    for instance in device_set.instances:
        new_instances.append(get_instance_in_time_of_day(instance,start_time,end_time))
    return appliance.ApplianceSet(new_instances,device_set.metadata)

def get_trace_windows(trace,window_length,window_step):
    """
    Returns a numpy array with stacked sliding windows of data from a trace.
    """
    print "WARNING: deprecated, "\
          "use trace.get_windows(window_length,window_step) instead"
    total_length = trace.series.size
    n_steps = int((total_length - window_length) / window_step)
    windows = []
    for step in range(n_steps):
        start = step * window_step
        window = trace.series[start:start + window_length].tolist()
        windows.append(window)
    return np.array(windows,dtype=np.float)

def traces_aligned(traces):
    """
    Returns True if traces are temporally aligned
    """
    indices = [trace.series.index for trace in traces]
    for index in indices[1:]:
        if not indices[0].summary()==(index.summary()):
            print index
            return False
    return True

def instances_aligned(instances):
    """
    Returns True iff instances and their traces are temporally aligned.
    """
    if len(instances) < 2:
        return True
    for instance in instances[1:]:
        if not len(instance.traces) == len(instances[0].traces):
            print "one"
            return False
    traces = map(list,zip(*[instance.traces for instance in instances]))
    for traces_ in traces:
        if not traces_aligned(traces_):
            print "two"
            return False
    return True

def align_traces(traces,to=None,how="front",freq=None):
    """
    Temporally aligns the traces. `how`="front" means to align to the front of
    the `to` trace. If no `to` trace is given, the first shortest trace is used.
    Traces are all downsampled to match the lowest sampling rate
    """
    # make copies

    traces=copy.deepcopy(traces)

    # if already aligned, don't do extra work.
    if traces_aligned(traces):
        return traces

    # resample to the same frequency

    if freq:
        new_freq = freq
    else:
        frequencies = [pd.tseries.frequencies.to_offset(trace.series.index.freq)
                    for trace in traces if trace.series.index.freq]
        try:
            new_freq = sorted(frequencies,reverse=True)[0]
        except IndexError:
            print "Please supply a frequency, no frequency could be guessed."

    for trace in traces:
        trace.resample(new_freq)

    # determine where to shift to and how much to cut off
    if not to:
        shortest_i = np.argsort([trace.series.size for trace in traces])[0]
        to = traces[shortest_i]
        cutoff = to.series.size
    else:
        all_traces = traces[:]
        all_traces.append(to)
        shortest_i = np.argsort([trace.series.size for trace in all_traces])[0]
        cutoff = all_traces[shortest_i].series.size

    # shift
    if how == 'front':
        offsets = [to.series.index[0] - trace.series.index[0] for trace in traces]
        for trace,offset in zip(traces,offsets):
            trace.series.index = trace.series.index + offset
    else:
        raise NotImplementedError

    # cut off extra:
    for trace in traces:
        trace.series = trace.series[:cutoff]

    return traces

def align_instances(instances):
    """
    Aligns all traces in a list of instances. Removes traces that don't fit.
    """
    traces = map(list,zip(*[instance.traces for instance in instances]))
    print traces
    aligned_traces = []
    for traces_ in traces:
        aligned_traces.append(align_traces(traces_))
    print aligned_traces
    traces = map(list,zip(*aligned_traces_))
    return [ApplianceInstance(traces_,instance.metadata)
            for traces_,instance in zip(traces,instances)]

