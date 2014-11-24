"""
Using the idl save file from the Kelly 2007 code linmix_err.pro, 
estimate the slope and error as well as the Nickel mass
"""
import numpy as np
import triangle
import sys

from scipy.io import readsav
from pack import hpd

rn=np.random.normal
def main():
	out_dict=readsav('../kelly_slope_intercept.sav', python_dict=True)
	
	inter=out_dict['post']['alpha']
	slope=out_dict['post']['beta']
	
	sn=sys.argv[1]
	
	f=np.loadtxt('../test/mcmc/redval.txt', dtype='string')
	v=f[f[:,0]==sn][0] 

	#return 0
	ar=[(inter[i]+slope[i]*rn(float(v[1]), float(v[2])))/rn(2.0, 0.3) for i in range(len(inter))]
	
	ar=np.array(ar)
	print "The median, upper and lower errors from the gibbs sampling are:",	np.median(ar), hpd.hpd(ar)[0]-np.median(ar), np.median(ar)-hpd.hpd(ar)[1] 

main()
