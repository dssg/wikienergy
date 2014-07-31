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
totals = np.sum(transitions,axis=2)[:,:,np.newaxis]
transitions = (transitions / totals)[:,:,:n_states-1]

mean_params = [pymc.Gamma('mean_param{}'.format(i), alpha=1, beta=.1) for i in range(n_states*2)]
var_params = [pymc.Gamma('var_param{}'.format(i), alpha=1, beta=.1) for i in range(n_states*2)]
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

    alpha = var_params[i*2]
    beta = var_params[i*2+1]
    var_obs.append(pymc.Gamma("var_obs{}".format(i),alpha=alpha,beta=beta,value=means[i],observed=True))
    var_pred.append(pymc.Gamma("var_pred{}".format(i),alpha=alpha,beta=beta))

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
M.sample(1000,200,10)
M.db.close()

