import theano
import theano.tensor as T
import numpy as np
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename",type=str,
    help="The filename of the pickled (trained) pylearn2 model. Ex) softmax.pkl")
args = parser.parse_args()

with open(args.filename,'r') as f:
    model = pickle.load(f)

X = model.get_input_space().make_theano_batch()
Y = model.fprop(X)

f = theano.function([X],Y)

test_input = np.array([[1,34,35,36,100],[300,200,0,19,188],[100,100,100,100,100]])

print f(test_input)

