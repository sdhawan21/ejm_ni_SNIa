import numpy as np
import sys
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d
from glob import glob

def bolpeak(fil):
	lc=np.loadtxt(fil)
	ter=interp1d(lc[:,0], lc[:,1], kind='cubic')
	l=np.linspace(lc[:,0].min(), lc[:,0].max())
	gpl=ter(l)
	return max(gpl)
	
def main():
	inf=sys.argv[1]
	sset=sorted(glob('../lcbol_distrib/finfiles/*.dat'))
	bp_arr=[]
	
	lbol=np.loadtxt('../tables/u_flags.txt', skiprows=1, usecols=(1, 2))
	for k in sset:
		bp=bolpeak(k)
		bp_arr.append(bp)
	bp_arr=np.array(bp_arr)
	plt.hist(bp_arr/1e43, alpha=0.3)
	plt.hist(lbol[:,0], alpha=0.3)
	plt.show()
	
main()
