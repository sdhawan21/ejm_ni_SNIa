#calculate the bolometric light curve from a set of filters for an SN.

"""
file format: like SN(oo)Py

inputs: currently, 
"""
from snpy import *
from scipy.interpolate import interp1d


import numpy as np
import matplotlib.pylot as plt
pt='/home/ug_msci2/CSP_files/snpy_trial/'
class bol_trans:
	def bol_lc_arr(sn, mu, e_mu, filt=None):
		#load SN; calculate the bolometric light curve (apparent flux)
		s=get_sn(pt+sn+'.snpy')
		if filt=None:
			bol=s.bolometric(s.filter_order)
		else:
			bol=s.bolometric(filt)
		mu2mpc=4*pi*(pow(10, (mu-25)/5.0)*3.08e24)**2
		
		#calculate errors on absolute flux
		dxx=bol[2]/bol[1]
		dyy=e_mu/mu
		
		
		#converted to absolute magnitudes
		bol[1]*=mu2mpc
		#final error (using dz/z=(dx/x  + dy/y))
		ebol=bol[1]*(dxx+dyy)
		#set all new values back in the old array
		bol[2]=ebol
	
		return bol
	def peakbol(sn, mu, filt=None)
		bol=bol_lc_arr(sn, mu, filt=None)
		gpl=interp1d(bol[0], bol[1], kind='cubic')
		l=np.linspace(min(bol[0], max(bol[0]), 100)
		sp=gpl(l)
		return l[sp==max(sp)], max(sp)

def main():
	#enter the SN and the distance modulus (currently done by hand)
	sn=sys.argv[1]
	mu=float(sys.argv[2])
	#evaluate the bolometric peak
	tmax, mmax=bol_trans().peakbol(sn, mu, filt=None)
main()

