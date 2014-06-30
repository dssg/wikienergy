import numpy as np
import math

def sum_error(truth,prediction):
    '''For a numpy array of truth values and prediction values returns the difference between their sums'''
    return math.fabs(truth.sum()-prediction.sum())

def evaluation_metric2(truth,prediction): # change these names
    return ####

def evaluate(truth,prediction):
   pass # run all metrics
