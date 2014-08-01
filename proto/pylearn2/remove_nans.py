import argparse
import numpy as np
import pylearn2.datasets as ds
import pickle
import os

parser = argparse.ArgumentParser()
parser.add_argument("data_dir",type=str,
    help="The relative directory where datasets are stored.")
parser.add_argument("dataset_prefix",type=str,
    help="The prefix of the dataset.")

args = parser.parse_args()

for name in ['train','valid','test']:
    with open(os.path.join(args.data_dir, args.dataset_prefix+'_'+ name + '.pkl'),'r') as f:
        dataset = pickle.load(f)

    dataset.X = np.nan_to_num(dataset.X)
    dataset.y = np.nan_to_num(dataset.y)

    with open(os.path.join(args.data_dir, args.dataset_prefix+'_'+ name + '.pkl'),'w') as f:
        pickle.dump(dataset,f)
