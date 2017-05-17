#calculate the Ni and ejecta mass for fast decliners
import numpy as np
import matplotlib.pyplot as plt

import sys

from glob import glob
from pack import bol,fid_time
from scipy.stats import pearsonr

bp=bol.bol_func().bolpeak

sne = np.loadtxt('all91bg.txt', dtype='string')#sorted(glob('bolometric/noir/*.dat'))

def vals_func(sn, suf='_lcbol_u_CSPB_CSPV_CSPr_CSPi_CSP.dat'):
	
	
	lc = np.loadtxt('bolometric/noir/'+sn+suf)

	mmax, tmax = bp('bolometric/noir/'+sn+suf)

	lc[:,0]-=tmax
	mni = mmax/2e43
	ft=fid_time.fid_time(mni)
	print "The estimated Ni mass is", mmax/2e43
	
	try:
		
		t0, mej, mni = ft.val_calc(sn, '/home/sdhawan/', 13, 'No')
	#	ft=fid_time.fid_time(mni)
		print "The fiducial timescale and total ejecta mass is:", t0, mej
		return mni, t0, mej
	except:
		return mni
vals = []
for i in sne:
	print i
	try:
		n, t, m = vals_func(i)
		vals.append([n, m])
	except:
		i
vals = np.array(vals)
print pearsonr(vals[:,0], vals[:,1]), len(vals)
plt.plot(vals[:,0], vals[:,1], 'gs')
plt.show()
