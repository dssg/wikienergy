import pylearn2
import pylearn2.datasets as ds
import pickle
import numpy as np

train_sets = []
valid_sets = []
test_sets = []

for i in range(5):
    with open("../../data/pylearn2/train_car_{:02d}.pkl".format(i),'r') as f:
        train_sets.append(pickle.load(f))
        
    with open("../../data/pylearn2/valid_car_{:02d}.pkl".format(i),'r') as f:
        valid_sets.append(pickle.load(f))

    with open("../../data/pylearn2/test_car_{:02d}.pkl".format(i),'r') as f:
        test_sets.append(pickle.load(f))

train_X = np.concatenate([train_set.X for train_set in train_sets], axis=0)
valid_X = np.concatenate([valid_set.X for valid_set in valid_sets], axis=0)
test_X = np.concatenate([test_set.X for test_set in test_sets], axis=0)
train_y = np.concatenate([train_set.y for train_set in train_sets], axis=0)
valid_y = np.concatenate([valid_set.y for valid_set in valid_sets], axis=0)
test_y = np.concatenate([test_set.y for test_set in test_sets], axis=0)

print train_X.shape
print valid_X.shape
print test_X.shape

train_set = ds.DenseDesignMatrix(X=train_X,y=train_y)
valid_set = ds.DenseDesignMatrix(X=valid_X,y=valid_y)
test_set = ds.DenseDesignMatrix(X=test_X,y=test_y)

with open("../../data/pylearn2/train_car_all.pkl",'w') as f:
    pickle.dump(train_set,f)
    
with open("../../data/pylearn2/valid_car_all.pkl",'w') as f:
    pickle.dump(valid_set,f)

with open("../../data/pylearn2/test_car_all.pkl",'w') as f:
    pickle.dump(test_set,f)
