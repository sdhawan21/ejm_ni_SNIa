import pymc as pm
import numpy as np

true_mu=1.5
true_tau=50.0
N_samp=500

mu=pm.Uniform('mu', lower=-100.0, upper=100.0)
tau=pm.Gamma('tau', alpha=0.1, beta=0.001)

data=pm.rnormal(true_mu, true_tau, size=(N_samp,))

y=pm.Normal('y', mu, tau, value=data, observed=True)









