import numpy as np
h=6.626e-27	#planck constant
k=1.38e-16	#boltzmann constant
c=2.997925e10	#speed of light
def plfn(lam, t=1e4):
	bet=(h*c)/(lam*t*k)
	den=np.exp(bet)-1
	num=2*h*(c**2)*(pow(lam, 5))
	return num/den
print plfn(0.4)*0.32








