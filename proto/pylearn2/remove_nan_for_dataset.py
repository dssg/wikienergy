import pickle
import numpy as np
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('filename',help="path to pickled file")
args = parser.parse_args()

with open(args.filename,'r') as f:
    file_ = pickle.load(f)

file_.X = np.nan_to_num(file_.X)
file_.y = np.nan_to_num(file_.y)

with open(args.filename,'w') as f:
    pickle.dump(file_,f)
