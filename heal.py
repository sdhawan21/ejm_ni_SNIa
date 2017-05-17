import matplotlib.pyplot as plt
import pylab
import numpy as np
import healpy as hp
import sys


NSIDE=128
LMAX=2*NSIDE

nbar=float(sys.argv[3])

clin =np.loadtxt ('../../lss_cl.dat')

def est_cl(nsamp, rad, fac):
	cdat=np.zeros(len(clin[:,1]))
	for k in range(nsamp):
		d_i=hp.synfast(clin[:,1], mmax=LMAX, lmax=LMAX, nside=NSIDE, new=True)
