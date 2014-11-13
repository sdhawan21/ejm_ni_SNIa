
import numpy as np
import matplotlib.pyplot as plt
import emcee
import sys


from src.mej_eq import mej
from pack import bol
lni=(1/8.8)
		
lco=(1/111.1)
		
fac=624150.647996
	
ds2=86400.0
def edp(t, Nni, t0):
	"""
	function for energy deposition; equation in Nadyozhin 1994
	"""
		
	
		
	#ENi
	t1=lni*Nni*np.exp(-lni*t)*(1.75)		
	#ECo_e+
	t2=lco*Nni*(lni/(lni-lco))*(np.exp(-lco*t)-np.exp(-lni*t))	
	#ECo_gamma
	t3=(0.12)+(3.61)*(1-np.exp(-(t0/t)**2))		
	return (t1+t2*t3)/(fac*ds2)#(t2*t3)/(fac*ds2)
	
numb=mej().numb
def lnprior(theta):
	
        if 15.0 < theta < 45.0:
		return 0.0
	return -np.inf

def lnlike(theta, x, y, yerr):
    t0	= theta
    Nni=numb(0.7)
    #ENi
    t1=lni*Nni*np.exp(-lni*t)*(1.75)		
    #ECo_e+
    t2=lco*Nni*(lni/(lni-lco))*(np.exp(-lco*t)-np.exp(-lni*t))	
    #ECo_gamma
    t3=(0.12)+(3.61)*(1-np.exp(-(t0/t)**2))		
    
    model=(t1+t2*t3)/(fac*ds2)
  
    #ex=m*(x+xerr)+b-m*(x)-b	
    return -0.5*(np.sum( ((y-model)**2./((yerr)**2))))

def lnprob(theta, x,  y, yerr):
    lp = lnprior(theta)
    if not np.isfinite(lp):
	return -np.inf
    return lp + lnlike(theta, x,   y, yerr)


def main():

	ndim=1
	nwalkers=200
	pos_min = np.array([15., 20.])
	pos_max = np.array([35., 40.])
	psize = pos_max - pos_min
	pos = [pos_min + psize*np.random.rand(ndim) for i in range(nwalkers)]
	
	filename=sys.argv[1]
	
	mjd, mag, magerr=np.loadtxt(filename, unpack=True)
	
	tmax=bol.bol_func().bolpeak(filename)[1]
	
	ph=mjd-tmax; cond=(ph>50) & (ph<100)
	ph1=ph[cond]; mag1=mag[cond]; magerr1=magerr[cond]
	
	
	
	sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=(ph1, mag1, magerr1))

	#burnin phase
	pos, prob, state  = sampler.run_mcmc(pos, 300)
	sampler.reset()

	import time
	time0 = time.time()


	pos, prob, state  = sampler.run_mcmc(pos, 700)

main()

