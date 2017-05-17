#calculate the ejecta mass using the functions from pack/

import numpy as np
import matplotlib.pyplot as plt
import sys

from scipy.interpolate import interp1d
from pack import bol, fid_time
from scipy.optimize import curve_fit

def peak(lc):
	spl = interp1d(lc[:,0], lc[:,1], kind='cubic')
	l = np.arange(lc[:,0].min(), lc[:,0].max(), 1)
	gl = spl(l)
	
	return max(gl), l[gl == max(gl)], gl,l
sn = sys.argv[1]
bp = bol.bol_func().bolpeak
f = 'bol/'+sn+'_lcbol_BVRI.dat'
snlc = np.loadtxt(f)

lmax, tmax, gl, l = peak(snlc)

"""
Very rough solution to the spline fitting issue, use the max for known well-sampled light curves

"""
tm = snlc[snlc[:,1] == max(snlc[:,1])][0][0]
snlc[:,0]-=tm
ni = max(snlc[:,1])/2e43
ft = fid_time.fid_time(ni)

l1 = snlc[(snlc[:,0] >40 ) & (snlc[:,0] < 100)]

popt, pcov = curve_fit(ft.edp_nomc, l1[:,0], l1[:,1], p0=[30.])

print popt[0], pcov, ft.ejm(popt[0]+13)

plt.plot(snlc[:,0], snlc[:,1], 'kD')
#plt.plot(l, gl, 'rs')
plt.show()
