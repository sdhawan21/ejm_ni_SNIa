import numpy as np
import matplotlib.pyplot as plt
import sys

from pack import bol
from glob import glob
from scipy.stats import pearsonr


#f=sys.argv[1]
def main():

	sset=sorted(glob("../lcbol_distrib/finfiles/*.dat"))
	#nm=np.loadtxt('../tables/u_flags.txt', dtype='string')[:,0]
	ld_arr=[]	
	mlate=[]	
	for k in sset:
		lc=np.loadtxt(k)
		bp=bol.bol_func().bolpeak(k)
		
		tmax=bp[1]
		mmax=bp[0]
		
		lc[:,0]-=tmax
	
		lc[:,1]/=1e43; lc[:,1]=2.5*np.log10(lc[:,1])	
	
		ld=bol.bol_func().late_decl(lc, ran=[40, 90])
		
		print ld[0]*55.0+ld[1]	
		#condition for late decline satisfied
		
		if ld[0]<99.0:	
				
			ld_arr.append([k, ld[0]])
			m55=ld[0]*55.0+ld[1]
			mlate.append([m55, mmax/1e43])	
	
	mlate=np.array(mlate)
	ldarr=np.array(ld_arr)
	print mlate, pearsonr(mlate[:,0], mlate[:,1])		
	np.savetxt("../out_files/bol_latedecline.txt", ldarr, fmt="%s")
main()
