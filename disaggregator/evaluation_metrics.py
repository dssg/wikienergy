"""
.. module:: evaluation_metrics
   :platform: Unix
   :synopsis: Contains methods for evaluating the performance of various
      machine learning algorithms used in disaggregation.

.. moduleauthor:: Sabina Tomkins <sabina@invalid.com>

"""

import numpy as np
import math
import scipy
import sys
from tabulate import tabulate

def sum_error(truth,prediction):
    '''
    Given a numpy array of truth values and prediction values, returns the
    absolute value of the difference between their sums.
    '''
    return math.fabs(truth.sum()-prediction.sum())

def get_index(app_instances,app):
    traces = app_instances.traces
    for t_i in range(len(traces)):
        if traces[t_i]==app:
           return t_i
    return -1


def fraction_energy_assigned_correctly(predicted_power_as_instances, ground_truth_as_instances):
    '''
        From NILMTK toolkit. Assumes that appliances are aligned in the sets.
    '''
    traces_truth = ground_truth_as_instances.traces
    #traces_power = [t.series for t in traces]
    traces_predicted = predicted_power_as_instances.traces
    #traces_predicted_power = [t.series for t in traces_predicted]
    total_energy_ground_truth = np.sum([float(np.sum(t.series)) for t in traces_truth])
    percent_power_by_app = np.array([])
    for trace_index in range(len(traces_predicted)):
        app_energy_predicted = np.sum(traces_predicted[trace_index].series)
        if traces_truth[trace_index].series.name==traces_predicted[trace_index].series.name:
            app_energy_ground_truth = np.sum(traces_truth[trace_index])
        else:
            index = get_index(predicted_power_as_instances,traces_predicted[trace_index].series.name)
            if index!=-1:
                app_energy_ground_truth = np.sum(traces_truth[index])
            else:
                app_energy_ground_truth = sys.maxint
        percent_power_by_app = np.append(percent_power_by_app,float(np.min([app_energy_predicted,app_energy_ground_truth])))
    return np.divide(float(np.sum(percent_power_by_app)),float(total_energy_ground_truth))

def rss(truth,prediction):
    '''Sum of squared residuals'''
    return np.sum(np.square(np.subtract(truth,prediction)))

def guess_truth_from_power(signals,threshold):
    '''
    Helper function for ground truth signals without on/off information.
    Given a series of power readings returns a numpy array where x[i]=0
    if signals[i] < threshold and x[i]=1 if signals[i] >= threshold
    '''
    return np.array([1 if i>=threshold else 0 for i in signals])

def get_positive_negative_stats(true_states, predicted_states):
    '''
    Returns a dictionary of numpy arrays containing the true positives a 'tp',
    the false negatives as 'fn', the true negatives as 'tn', and
    the false positives as 'fp'. I would like
    to make this a truth table instead of putting the logic directly in the
    list comprehension.
    '''
    pos_neg_stats={}
    pos_neg_stats['tp'] = np.array([a and b for (a,b) in zip(true_states,predicted_states)])
    pos_neg_stats['fn'] = np.array([1 if a==1 and b==0 else 0 for (a,b) in zip(true_states,predicted_states)])
    pos_neg_stats['tn'] = np.array([1 if a==0 and b==0 else 0 for (a,b) in zip(true_states,predicted_states)])
    pos_neg_stats['fp'] = np.array([1 if a==0 and b==1 else 0 for (a,b) in zip(true_states,predicted_states)])
    return pos_neg_stats

def get_sensitivity(true_positives,false_negatives):
    '''
    Given a numpy array of true positives, and false negatives returns a
    sensitivty measure. Then the sensitivity is equal to TP/(TP+FN), where TP
    is a true positive, such that TP=1 when the predicted value was correctly
    classified as positive and 0 otherwise and FN is false negative, such that
    FN = 1 if a value was falsely predicted to be negative and 0 otherwise.
    '''
    return float(true_positives.sum())/(true_positives.sum()+false_negatives.sum())

def get_specificity(true_negatives, false_positives):
    '''
    Given a numpy array of true negatives, and false positives returns a
    specificty measure. The specificity measure is equal to TN/(TN+FP), where
    TN is a true negative, such that TN=1 when the predicted value was
    correctly classified as negative and 0 otherwise and FP is a false
    positive, such that FP = 1 if a value was falsely predicted to be positive
    and 0 otherwise.
    '''
    return float(true_negatives.sum())/(true_negatives.sum()+false_positives.sum())

def get_precision(true_positives,false_positives):
    '''Given a numpy array of true positives, and false positives returns a
    precision measure. The precision measure is equal to TP/(TP+FP), where TP
    is a true positive, such that TP=1 when the predicted value was correctly
    classified as positive and 0 otherwise and FP is a false positive, such
    that FP = 1 if a value was falsely predicted to be positive and 0
    otherwise.
    '''
    return float(true_positives.sum())/(true_positives.sum()+false_positives.sum())


def get_accuracy(stats):
    '''
        Takes an array of true positives, false negatives, true negatives, and false positives. Returns the Accuracy measure where accuracy is tp+tn/(tn+fn+tp+fp)
    '''
    return (stats['tp']+stats['tn'])/sum(stats)

def get_table_of_confusion(true_negatives, true_positives, false_negatives, false_positives):
    row_one = ["Positive",true_positives.sum(),false_positives.sum()]
    row_two = ["Negative", false_negatives.sum(), true_negatives.sum()]
    headers = ["Positive","Negative"]
    table = [row_one,row_two]
    return tabulate(table,headers,tablefmt = "grid")



