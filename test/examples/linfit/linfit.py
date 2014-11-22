import pymc as pm
import numpy as np

import pylab

slp=1.5
intc=4.0
N=30

true_x= pm.runiform(0, 50, N)
true_y = slp*true_x + intc

data_y=pm.rnormal(true_y, 2)

data_x=rnormal(true_x, 2)

def theta(value=array([2.,5.])):
    """Slope and intercept parameters for a straight line.
    The likelihood corresponds to the prior probability of the parameters."""
    slope, intercept = value
    prob_intercept = pm.uniform_like(intercept, -10, 10)
    prob_slope = np.log(1./np.cos(slope)**2)
    return prob_intercept+prob_slope

init_x=data_x.clip(min=0, max=50)

x=pm.Uniform('x', lower=0, upper=50, value=init_x)




































