import pickle
import argparse
import os
import pylearn2.datasets as ds
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("data_dir", help="data directory")
parser.add_argument("old_prefix", help="prefix for old files")
parser.add_argument("new_prefix", help="prefix for new files")
args = parser.parse_args()

for name in ["train","valid","test"]:
    old_filename = os.path.join(args.data_dir,args.old_prefix + "_" + name + ".pkl")
    new_filename = os.path.join(args.data_dir,args.new_prefix + "_" + name + ".pkl")
    with open( old_filename,'r') as f:
        dataset = pickle.load(f)

    new_dataset_X = []
    new_dataset_y = []
    for input_array,class_array in zip(dataset.X,dataset.y):
        class_ = np.argmax(class_array)
        if not class_ == 0:
            new_dataset_X.append(input_array)
            new_dataset_y.append(class_array)

    new_dataset = ds.DenseDesignMatrix(X = np.array(new_dataset_X),y=np.array(new_dataset_y))

    with open( new_filename,'w') as f:
        pickle.dump(new_dataset,f)
