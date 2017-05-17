import numpy as np
import matplotlib.pyplot as plt
import sys

from pack import bol, fid_time
from glob import glob
from scipy.optimize import curve_fit
from scipy.stats import pearsonr
bp=bol.bol_func().bolpeak

bollc = sorted(glob('bolometric/*.dat'))

mni = [bp(i)[0]/2e43 for i in bollc]

mej =[]; names=[]
for i in bollc:
	
	lc = np.loadtxt(i)
	b=bp(i)
	tmax = b[1]
	

	if tmax > 99:
		lc[:,0]-=tmax
		
		mni = b[0]/2e43
		
		
		def_fid=fid_time.fid_time(mni)
		lc1 = lc[(lc[:,0]>50) & (lc[:,0] < 100)]	
		if len(lc1) >= 3:		
			popt, pcov = curve_fit(def_fid.edp_nomc, lc1[:,0], lc1[:,1], p0=[20.] )		
			ejm = def_fid.ejm(popt[0]+19)
			
			mej.append([mni, ejm])
			names.append([mni, ejm, i[11:19]])

mej= np.array(mej); print names
print pearsonr(mej[:,0], mej[:,1]), len(mej)
plt.plot(mej[:,0], mej[:,1], 'rs')
#plt.show()
