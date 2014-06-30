import sys
sys.path.append('../')
#print sys.path

import numpy as np
from disaggregator import evaluation_metrics as evm

def main():
    truth = np.ones(7)
    prediction = np.zeros(7)
    print evm.sum_error(truth,prediction)

if __name__=='__main__':
    main()