from scipy.interpolate import interp1d

import numpy as np

rn=np.random.normal
def h0_sne(M, zp):
	"""
	Hubble constant from SNe observed in different passbands

	"""
	val=M+25-zp
	h0=pow(10, 0.2*val)
	return h0

def h0_mc(M, zp, n):
	arr=np.array([h0_sne(rn(M[0], M[1]), rn(zp[0], zp[1])) for k in range(n)])
	return np.mean(arr), np.std(arr)








