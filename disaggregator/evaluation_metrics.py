import numpy as np
import math
import scipy

def sum_error(truth,prediction):
    '''
    Given a numpy array of truth values and prediction values, returns the
    absolute value of the difference between their sums.
    '''
    return math.fabs(truth.sum()-prediction.sum())

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
    Returns a list of series where the first series is the true positives,
    the second series is the false negatives, the third series is the true
    negatives and the fourth series is the false positives. I would like
    to make this a truth table instead of putting the logic directly in the
    list comprehension.
    '''
    true_positives = np.array([a and b for (a,b) in zip(true_states,predicted_states)])
    false_negatives = np.array([1 if a==1 and b==0 else 0 for (a,b) in zip(true_states,predicted_states)])
    true_negatives = np.array([1 if a==0 and b==0 else 0 for (a,b) in zip(true_states,predicted_states)])
    false_positives = np.array([1 if a==0 and b==1 else 0 for (a,b) in zip(true_states,predicted_states)])
    return [true_positives,false_negatives,true_negatives,false_positives]

def get_sensitivity(true_positives,false_negatives):
    '''
    Given a numpy array of true positives, and false negatives returns a
    sensitivty measure. Then the sensitivity is equal to TP/(TP+FN), where TP
    is a true positive, such that TP=1 when the predicted value was correctly
    classified as positive and 0 otherwise and FN is false negative, such that
    FN = 1 if a value was falsely predicted to be negative and 0 otherwise.
    '''
    return true_positives.sum()/(np.sum(true_positives.sum(),false_negatives.sum()))

def get_specificity(true_negatives, false_positives):
    '''
    Given a numpy array of true negatives, and false positives returns a
    specificty measure. The specificity measure is equal to TN/(TN+FP), where
    TN is a true negative, such that TN=1 when the predicted value was
    correctly classified as negative and 0 otherwise and FP is a false
    positive, such that FP = 1 if a value was falsely predicted to be positive
    and 0 otherwise.
    '''
    return true_negatives.sum()/(np.sum(true_negatives.sum(),false_positives.sum()))

def get_precision(true_positives,false_positives):
    '''Given a numpy array of true positives, and false positives returns a
    precision measure. The precision measure is equal to TP/(TP+FP), where TP
    is a true positive, such that TP=1 when the predicted value was correctly
    classified as positive and 0 otherwise and FP is a false positive, such
    that FP = 1 if a value was falsely predicted to be positive and 0
    otherwise.
    '''
    return true_positives.sum()/(np.sum(true_positives.sum(),false_positives.sum()))


def get_accuracy():
    pass
