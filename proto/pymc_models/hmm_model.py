import pymc
import numpy as np


trans = [[80,10,10],[10,80,10],[10,10,80]]
n_samples = 1000
means = [pymc.rgamma(alpha,beta,size=n_samples) for alpha,beta in zip([1,2,3],[0.1,0.2,0.3])]
variances = [pymc.rgamma(alpha,beta,size=n_samples) for alpha,beta in zip([.2,.3,.4],[0.1,0.1,0.1])]
transitions = [pymc.rdirichlet(trans_,size=n_samples) for trans_ in trans]


n_gamma = 3
n_modes = n_gamma * 2
mean_params = [pymc.Gamma('mean_param{}'.format(i), alpha=1, beta=.1) for i in range(n_modes)]
var_params = [pymc.Gamma('var_param{}'.format(i), alpha=1, beta=.1) for i in range(n_modes)]
trans_params = [pymc.Beta('trans_params{}'.format(i), alpha=1,beta=1) for i in range(n_gamma*n_gamma)]


mean_obs = []
mean_pred = []
var_obs = []
var_pred = []
trans_obs = []
trans_pred = []

for i in xrange(n_gamma):
    alpha1 = mean_params[i*2]
    beta1 = mean_params[i*2+1]
    mean_obs.append(pymc.Gamma("mean_obs{}".format(i),alpha=alpha1,beta=beta1,value=means[i],observed=True))
    mean_pred.append(pymc.Gamma("mean_pred{}".format(i),alpha=alpha1,beta=beta1))

    alpha2 = var_params[i*2]
    beta2 = var_params[i*2+1]
    var_obs.append(pymc.Gamma("var_obs{}".format(i),alpha=alpha2,beta=beta2,value=variances[i],observed=True))
    var_pred.append(pymc.Gamma("var_pred{}".format(i),alpha=alpha2,beta=beta2))

    prob1 = trans_params[i*3]
    prob2 = trans_params[i*3+1]
    prob3 = trans_params[i*3+2]
    @pymc.deterministic
    def params(a=prob1,b=prob2,c=prob3):
        return np.array([a,b,c])
    trans_obs.append(pymc.Dirichlet("trans_obs{}".format(i),params,value=transitions[i],observed=True))
    trans_pred.append(pymc.Dirichlet("trans_pred_incomplete{}".format(i),params))

pred = mean_pred[:]
pred.extend(var_pred)
pred.extend(trans_pred)
model = pymc.Model(pred)
