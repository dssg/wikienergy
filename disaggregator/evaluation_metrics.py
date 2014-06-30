import numpy as np
import math
import scipy

def sum_error(truth,prediction):
    '''For a numpy array of truth values and prediction values returns the absolute value of the difference between their sums'''
    return math.fabs(truth.sum()-prediction.sum())

def rss(truth,prediction):
    '''sum of squared residuals'''
    
    return np.sum(np.square(np.subtract(truth,prediction)))

def evaluate(truth,prediction):
   pass # run all metrics
