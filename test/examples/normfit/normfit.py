import pymc as pm
import numpy as np
import simple

model=pm.MCMC(simple)
model.sample(iter=1000, burn=500, thin=2)













