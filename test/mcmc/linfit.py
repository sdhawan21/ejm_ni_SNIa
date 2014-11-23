"""
Bayesian parameter estimatino for linear regression.

Uses affine invariant mcmc package called emcee (Foreman-Mackey+ 2012/13)
More theory in Hogg + 2010

Explanation for why bayesian parameter estimation is unbiased see Kelly+ 2007

Uses highest posterior density for best estimate, NOT mean (hpd from biopython)



Arguments 
	1: file with input parameters (lmax, elmax, t2, et2)
	2: Name of SN for which Ni 56 mass is to be calculated
	3: Whether any cuts on the flags are to be made


Output:
	The printed outputs should be explanatory, nonetheless
	1. upper, lower errors & slope
	2 ."" "" "" intercept
	3. & 4. Nickel mass from samples (mean and std), same but with hpd and asymmetric errors

Author: Suhail Dhawan, ESO (jeez, do you have to)


"""

import numpy as np
import emcee
import matplotlib.pyplot as plt

import sys 
#import pymc as pc

#hpd is the highest posterior density and confidence interval calculation routine. For asymmetric errors and non-gaussian distributions
from pack.hpd import hpd
from scipy.stats import skew

import triangle



def main():
	"""
	everything written in main function. Doesnt seem to be optimal structure
	"""
	infile=np.loadtxt(sys.argv[1], usecols=(1, 2, 3, 6, 5), skiprows=1)
	
	#uses the "v. low reddening flags"
	#load the last column of the file which gives the Y/N flags	
	fl=np.loadtxt(sys.argv[1], usecols=(0, -1), skiprows=1, dtype='string')[:,1]

	#do you want to use the flags?
	if sys.argv[3]=='fl':
		infile=infile[fl=='Y']
	ndim = 2
	nwalkers = 200


	#define input arrays for the data
	x=infile[:,-1]; xerr=infile[:,-2]

	y=infile[:,0]; yerr=infile[:,1]

	#uniform prior (Jeffreys prior) with strict cutoff
	#prior on slope is between -10 to 10 and -10 to 15 for intercept
	def lnprior(theta):
	    m, b = theta
	    if -10.0 < m < 10.0 and -10.0 < b < 15.0:
		return 0.0
	    return -np.inf

	# As likelihood, we assume the chi-square. Note: we do not even need to normalize it.

	def lnlike(theta, x,xerr,  y, yerr):
	    m, b = theta
	    model = m * (x) + b
	    ex=m*(x+xerr)+b-m*(x)-b	
	    return -0.5*(np.sum( ((y-model)**2./((yerr)**2.))))


	#using bayes' theorem log posterior= logprior +loglikelihood
	def lnprob(theta, x, xerr, y, yerr):
	    lp = lnprior(theta)
	    if not np.isfinite(lp):
		return -np.inf
	    return lp + lnlike(theta, x,  xerr, y, yerr)





	pos_min = np.array([-5., 0.])
	pos_max = np.array([5., 10.])
	psize = pos_max - pos_min
	pos = [pos_min + psize*np.random.rand(ndim) for i in range(nwalkers)]

	sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=(x, xerr, y, yerr))

	#burnin phase
	pos, prob, state  = sampler.run_mcmc(pos, 300)
	sampler.reset()

	import time
	time0 = time.time()


	pos, prob, state  = sampler.run_mcmc(pos, 700)

	time1=time.time()

	print "Sampling time in seconds is: \t", time1-time0, '\n'





	#sys.exit()

	samples=sampler.flatchain

	#print samples[-100:]


	xl = np.linspace(x.min(), x.max())
	m=samples[:,0]; b=samples[:,1]

	#m_mcmc,b_mcmc=map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]), zip(*np.percentile(samples, [16, 50, 84], axis=0)))
	#print "errors ", m_mcmc, b_mcmc

	print "Upper and lower errors on slope and highest posterior density: \t", hpd(m)[0]-np.median(m), hpd(m)[1]-np.median(m), np.median(m),'\n'

	print "Upper and lower errors on intercept and highest posterior density: \t", hpd(b)[0]-np.median(b), hpd(b)[1]-np.median(b), np.median(b), '\n' 
	rn=np.random.normal

	val_table=np.loadtxt('redval.txt', dtype='string')

	sn=sys.argv[2]

	t2=float(val_table[val_table[:,0]==sn][0][1]); et2=float(val_table[val_table[:,0]==sn][0][2])
	
	def t2val(t2, et2):
		ar=[(samples[i][0]*rn(t2, et2)+samples[i][1])/rn(2.0, 0.3) for i in range(len(samples))]
		return ar
	fig=triangle.corner(samples, label=['m', 'b'], truths=[hpd(samples[:,0])[1], hpd(samples[:,1])[1]])

	#np.savetxt('out/samples_mb.txt', samples)
	vals=t2val(t2, et2)

	bf=(hpd(vals)[0]+hpd(vals)[1])/2.0

	print "The value of radioactive Nickel mass estimated is: \t",  np.mean(vals), np.std(vals), '\n'

	print "Asymmetric error bars for Nickel mass (using hpd): \t", np.median(vals), np.median(vals)-hpd(vals)[0], hpd(vals)[1]-np.median(vals), '\n'

	#print "Skewness of values is \t:", skew(vals)

	plt.figure(2)

	plt.hist(vals)
	#print "Acceptance fraction \t:", sampler.acceptance_fraction, sampler.acceptance_fraction.shape
	#plt.show()




	"""
	for m, b in samples[-100:]: # samples[np.random.randint(len(samples[-100), size=100)]:
	    plt.plot(xl, m*xl+b, color="k", alpha=0.1)
	plt.errorbar(x, y, yerr=yerr, fmt=".k")
	plt.show()
	"""
if len(sys.argv)==4:
	main()
else:
	print "Usage: python" +sys.argv[0]+ "<file with parameters> <SN>  <filtering the sample?>"

