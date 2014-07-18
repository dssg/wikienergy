from pymc import Gamma, Normal, Dirichlet

mean1 = Gamma("mean1",alpha=0.1,beta=1)
mean2 = Gamma("mean1",alpha=100,beta=1)
mean3 = Gamma("mean1",alpha=200,beta=1)

covar1 = None
