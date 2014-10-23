from scipy.interpolate import interp1d

import numpy as np

rn=np.random.normal
def spl_fit(arr, val):
	"""
	interpolate value for Nickel mass
	"""
	real=rn(arr[:,0], arr[:,1])
	terp=interp1d(real, rn(arr[:,2], arr[:,3]), kind='cubic')
	l=np.linspace(real.min(), real.max())
	gpl=terp(l)
	l1=abs(l-val)
	return gpl[l1==min(l1)][0]












