from pylearn2.expr.nnet import (compute_precision, compute_recall, compute_f1)
from pylearn2.utils import serial
import theano
import numpy as np
import argparse
import sys
import os
sys.path.append(os.path.join(os.pardir,os.pardir))
from disaggregator import evaluation_metrics
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("saved_model",type=str,
    help="The relative path to the saved model.")
parser.add_argument("test_set",type=str,
    help="The relative path to the testing set.")
args = parser.parse_args()

model = serial.load(args.saved_model)
test_data = serial.load(args.test_set)

X = model.get_input_space().make_theano_batch()
Y = model.fprop(X)
f = theano.function([X],Y,allow_input_downcast=True)

y = theano.shared(test_data.y)
outputs = f(test_data.X[:,:,np.newaxis,np.newaxis])
y_hat = outputs > 0.5

def get_tp_fp_tn_fn(y_hat,y):
    tp = (y[:,1].eval() * y_hat[:,1]).sum()
    tn = ((y[:,0].eval()) * y_hat[:,0]).sum()
    p = y[:,1].eval().sum()
    n = y[:,0].eval().sum()
    return tp,p-tp,tn,n-tn

tp,fp,tn,fn = get_tp_fp_tn_fn(y_hat,y)

print
print "    |   t   |   f   | (actual)"
print "  t | {} | {} |".format(tp,fp)
print "  f | {} | {} |".format(fn,tn)
print "(pred)"
print "total: {}".format(tp+fp+tn+fn)
print

precision = evaluation_metrics.get_precision(tp,fp)
recall = evaluation_metrics.get_sensitivity(tp,fn)
f1 = 2*precision*recall/(precision+recall)

print 'precision: {0}'.format(precision)
print 'recall: {0}'.format(recall)
print 'f1: {0}'.format(f1)

y_hats = [outputs > p for p in np.linspace(0,1,51,endpoint=True)]

precisions = []
recalls = []
for y_ in y_hats:
    tp,fp,tn,fn = get_tp_fp_tn_fn(y_,y)
    prec = evaluation_metrics.get_precision(tp,fp)
    rec = evaluation_metrics.get_sensitivity(tp,fn)
    precisions.append(prec)
    recalls.append(rec)


plt.plot(precisions,recalls)
plt.show()
