import pylearn2
import pylearn2.datasets as ds
import numpy as np
from sklearn import hmm
import os
import pickle

def build_dataset(model,length,window_size,label_index,num_classes):
    all_data = []
    all_labels = []
    data,labels = model.sample(length)
    data = data.T[0]
    labels = labels.T
    for i in range(length - window_size + 1):
        all_data.append(data[i:i+window_size])
        label_one_hot = np.zeros(num_classes)
        label_one_hot[labels[i+label_index]] = 1
        all_labels.append(label_one_hot)
    return zip(np.array(all_data), np.array(all_labels).astype(int))
        
def get_train_valid_test(dataset,n_train,n_valid,n_test):
    dataset_copy = dataset[:]
    np.random.shuffle(dataset_copy)
    assert(len(dataset_copy) >= n_train + n_valid + n_test)
    train = dataset_copy[:n_train]
    valid = dataset_copy[n_train:n_train+n_valid]
    test = dataset_copy[n_train + n_valid:n_train+n_valid+n_test]
    return train, valid, test

def convert_to_pylearn_ds(train,valid,test):
    train_X, train_y = map(np.array,zip(*train))
    valid_X, valid_y = map(np.array,zip(*valid))
    test_X, test_y = map(np.array,zip(*test))

    # convert to pylearn_dataset
    return ds.DenseDesignMatrix(X=train_X,y=train_y),\
        ds.DenseDesignMatrix(X=valid_X,y=valid_y),\
        ds.DenseDesignMatrix(X=test_X,y=test_y)

def fake_hmm_appliance(pi,a,mean,cov):
    model=hmm.GaussianHMM(pi.size, "full", pi,a)
    model.means_ = mean
    model.covars_ = cov
    return model

def export_datasets(path,datasets, names):
    for name,dataset in zip(names,datasets):
        with open(os.path.join(path,name + '.pkl'), 'w') as f:
            pickle.dump(dataset,f)
    
if __name__ == "__main__":
    # create a fake A/C
    pi=np.array([0.1,0.9])
    a=np.array([[0.95,0.05],[0.05,0.95]])
    mean=np.array([[0],[1500]])
    cov=np.array([[[ 1.]],[[ 10]]])
    model = fake_hmm_appliance(pi,a,mean,cov)

    # randomly sample one day of data and format it as a pylearn2 dataset
    dataset = build_dataset(model,96,5,2,2)
    train, valid, test = get_train_valid_test(dataset,48,22,22)
    train,valid,test = convert_to_pylearn_ds(train,valid,test)

    # export datasets
    export_datasets("/home/pngo/data",[train,valid,test],["train_fake_ac_day","valid_fake_ac_day","test_fake_ac_day"])
