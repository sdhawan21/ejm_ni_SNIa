from scipy.interpolate import interp1d

import numpy as np

rn=np.random.normal
c=2.997924562e5
def h0_sne(M, zp):
	"""
	Hubble constant from SNe observed in different passbands

	"""
	val=M+25-zp
	h0=pow(10, 0.2*val)
	return h0

def h0_mc(M, zp, n):
	"""
	Monte carlo to estimate H0 given the absolute magnitude the SNae zero point in a given filter for an Sn (with n realizations )

	"""

	arr=np.array([h0_sne(rn(M[0], M[1]), rn(zp[0], zp[1])) for k in range(n)])
	return np.mean(arr), np.std(arr)

def h0_withcosm(dl, z, om=0.27, ol=0.73):
	"""
	
	Using the complete expression for h0 with values of omega_m and omega_lambda, for low z  this approaches the nocosm value 
	om=0.27, ol=0.73 default
	"""
	q0=(om/2)-ol
	a=z*(1-q0)/(np.sqrt(1+2*q0*z)+1+q0*z )
	h0=(1+a)*c*z/dl
	return h0

def h0_nocosm(dl, z):
	return c*z/dl 
def arr_crt(fil1, fil2):
	"""	
	From two files create arrays of the parameter values for SN present in both
	"""
	a1=np.loadtxt(fil1, dtype='string')
	a2=np.loadtxt(fil2, dtype='string')

	arr1=[float(i[1]) for i in a1 if i[0] in a2[:,0]]
	arr2=[float(a2[a2[:,0]==i[0]][0][1]) for  i in a1  if i[0] in a2[:,0] ]

	return arr1, arr2

def lum_dist(z, om=0.27, ol=0.73, h0=70):
	q0=(om/2)-ol
	a=z*(1-q0)/(np.sqrt(1+2*q0*z)+1+q0*z )
	dl=(1+a)*c*z/h0
	return dl

def rev_arr_crt(fil1, fil2, n):
	"""	
	From two files create arrays of the parameter values for SN present in both
	"""
	a1=np.loadtxt(fil1, dtype='string', delimiter='&')
	a2=np.loadtxt(fil2, dtype='string', delimiter='&')

	nm=np.array([i[0][:-1] for i in a2])

	arr1=[i[n][2:6] for i in a1 if 'SN'+i[0][:-1] in nm]
	
	arr2=[float(a2[nm=='SN'+i[0][:-1]][0][3]) for  i in a1  if 'SN'+i[0][:-1] in nm ]
	
	f1=[]; f2=[]
	for k in range(len(arr1)):
		try:
			f1.append(float(arr1[k]))
			f2.append(float(arr2[k]))
		except:
			arr1[k]	
	return np.array(f1), np.array(f2)
def self_arr_crt(fil1, fil2, n, n1):
	"""	
	From two files create arrays of the parameter values for SN present in both
	"""
	a1=np.loadtxt(fil1, dtype='string', delimiter='&')
	a2=np.loadtxt(fil2, dtype='string', delimiter='&')

	#nm=np.array([i[0][:-1] for i in a2])

	arr1=[i[n][2:6] for i in a1 if i[0] in a2[:,0]]
	
	arr2=[a2[a2[:,0]==i[0]][0][n1][2:6] for  i in a1  if i[0] in a2[:,0] ]
	
	f1=[]; f2=[]
	for k in range(len(arr1)):
		try:
			finp=float(arr1[k])
			finp2=float(arr2[k])
			f1.append(finp)
			f2.append(finp2)
		except:
			arr1[k]	
	return np.array(f1), np.array(f2)	


