import pymc
import numpy as np
import argparse
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("in_file", type=str, help="Input files")
parser.add_argument("out_file", type=str, help="Output files")
args = parser.parse_args()

with open(args.in_file,'r') as f:
    hmm_models = pickle.load(f)['air1'].values()

means = [ hmm.means_.T[0] for hmm in hmm_models]
variances = [ hmm.covars_.T[0,0] for hmm in hmm_models]
transitions = [ hmm.transmat_ for hmm in hmm_models]

n_states = 3

means = np.array(zip(*means)).clip(0.001)
variances = np.array(zip(*variances))#.clip(0.001)
transitions = np.array(zip(*transitions))
totals = np.sum(transitions,axis=2)
new_shape = list(totals.shape)
new_shape.append(1)
transitions = (transitions / totals.reshape(new_shape))[:,:,:n_states-1]

for i in range(3):
    print means[i]
    print
    print variances[i]
    print
    print transitions[i]
    print

mean_params = [pymc.Gamma('mean_param{}'.format(i), alpha=1, beta=.1) for i in range(n_states*2)]
var_params = [pymc.Uniform('var_param{}'.format(i), lower=0, upper=1) for i in range(n_states*2)]
trans_params = [pymc.Beta('trans_params{}'.format(i), alpha=1, beta=1) for i in range(n_states**2)]

mean_obs = []
mean_pred = []
var_obs = []
var_pred = []
trans_obs = []
trans_pred = []

for i in xrange(n_states):
    alpha = mean_params[i*2]
    beta = mean_params[i*2+1]
    mean_obs.append(pymc.Gamma("mean_obs{}".format(i),alpha=alpha,beta=beta,value=means[i],observed=True))
    mean_pred.append(pymc.Gamma("mean_pred{}".format(i),alpha=alpha,beta=beta))

    mu = var_params[i*2]
    tau = var_params[i*2+1]
    var_obs.append(pymc.Normal("var_obs{}".format(i),mu=mu,tau=tau,value=variances[i],observed=True))
    var_pred.append(pymc.Normal("var_pred{}".format(i),mu=mu,tau=tau))

    probs = [trans_params[i*n_states + j] for j in range(n_states)]
    @pymc.deterministic
    def params(probs=probs):
        return np.array(probs)

    trans_obs.append(pymc.Dirichlet("trans_obs{}".format(i),params,value=transitions[i],observed=True))
    trans_pred.append(pymc.Dirichlet("trans_pred{}".format(i),params))

pred = mean_pred[:]
pred.extend(var_pred)
pred.extend(trans_pred)
model = pymc.Model(pred)

M = pymc.MCMC(model)
M.sample(10000,2000,10)

import pdb;pdb.set_trace()
with open(args.out_file,'w') as f:
    pickle.dump(M,f)
