import os.path
import sys
sys.path.append(os.path.join(os.pardir,os.pardir))
from disaggregator import fhmm
from disaggregator import utils
import pymc
import argparse
import random
import numpy as np
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument("in_file", type=str, help="pickled model file")
parser.add_argument("out_file", type=str, help="pickled model file")
args = parser.parse_args()

n_states = 3
db = pymc.database.pickle.load(args.in_file)
M = pymc.MCMC(db=db)

def get_hmm():
    sample = random.randint(0,80)
    means = np.array([ M.trace('mean_pred{}'.format(i), chain=None)[sample]
        for i in range(n_states)])
    covars = np.array([ M.trace('var_pred{}'.format(i), chain=None)[sample]
        for i in range(n_states)])
    trans = np.array([ M.trace('trans_pred{}'.format(i), chain=None)[sample]
        for i in range(n_states)])
    trans = np.concatenate([trans,(np.ones(3) - trans.sum(axis=1))[:,np.newaxis]],axis=1)
    cov = utils.trace_series_to_numpy_array(pd.Series(covars))
    hmm = fhmm.init_HMM(trans[0],trans,means[:,np.newaxis],covars[:,np.newaxis,np.newaxis])
    return hmm
hmm = get_hmm()

M.db.close()
