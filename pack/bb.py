import numpy as np

class bb_func:
	h = 6.634e-27
	k= 1.38e-16
	c=3e10

	def bb_lam(self, lam, T=8000):
		h=self.h; c=self.c; k=self.k
		
		fac=2*h*c**2/(lam**5)
		den = np.exp(h*c/(lam*k*T)) -1
		return fac/den 





