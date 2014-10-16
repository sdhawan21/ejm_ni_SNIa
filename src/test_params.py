import numpy as np
import sys
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d
from glob import glob

rn=np.random.normal

def bolpeak(fil):
	lc=np.loadtxt(fil)
	ter=interp1d(lc[:,0], lc[:,1], kind='cubic')
	l=np.linspace(lc[:,0].min(), lc[:,0].max())
	gpl=ter(l)
	return max(gpl)
def err_bolpeak(fil):
	maxar=[]
	
	#take 1000 realisations of the light curve
	for k in range(1000):
		lc=np.loadtxt(fil)
		real=rn(lc[:,1], lc[:,2]) 
		
		#interpolation routine written within scipy, as Marco says "its fucknig amazing"
	
		ter=interp1d(lc[:,0], real, kind='cubic')
		l=np.linspace(lc[:,0].min(), lc[:,0].max())
		gpl=ter(l)
		maxar.append(max(gpl))
	
	return np.array(maxar) 
def main():
	#infile, if from command line
	if len(sys.argv)==2:
		inf=sys.argv[1]

	sset=sorted(glob('../lcbol_distrib/finfiles/*.dat'))
	
	bp_arr=[]
	
	nmarr=[]
	
	lbol=np.loadtxt('../tables/u_flags.txt', skiprows=1, usecols=(1, 2))
	
	for k in sset:
	
		bp=bolpeak(k)
	
		bp_arr.append(bp)
	
		nmarr.append([k, np.std(err_bolpeak(k)/1e43)])
	
	#return 0
	bp_arr=np.array(bp_arr)
	plt.hist(bp_arr/1e43, alpha=0.3)
	plt.hist(lbol[:,0], alpha=0.3)
	plt.show()
	
main()
