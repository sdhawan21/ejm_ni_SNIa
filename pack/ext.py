import numpy as np

from scipy.integrate import simps

class ccm:
	def __init__(self, rv, av):
		self.av=av
		self.rv=rv
	def a(self, lam):
		x=1./lam
		if x >= .3 and x <= 1.1:
			a= .574* pow(x, 1.61)
		elif x >= 1.1 and x <= 3.3:
			y= x -1.82
			a=1 + .17699 *y - .50447*y**2 - 0.02427* y**3 +.72085*y **4 + 0.01979*y**5 - 0.77530*y**6 + 0.32999*y**7			
		else:
			print "x is not in range"
		return a 		

	def b(self, lam):
		x=1./lam
		if x >= .3 and x <= 1.1:
			b= -0.527 * pow(x, 1.61)
		elif x >= 1.1 and x <= 3.3:
			y= x-1.82
			b = 1.41338*y + 2.28305*y**2 + 1.07233*y**3 - 5.38434*y**4 - 0.62251*y**5 + 5.30260* y**6 - 2.09002*y**7
		else: 
			print "x is not in range"
		return b
		
	def alam(self, lam):
		alav=self.a(lam)+self.b(lam)/self.rv
		al=alav*self.av
		return al


class pow_law:
	def __init__(self, av, indexx):
		self.av=av
		self.indexx = indexx
	
	def alam(self, lam):
		t= self.av*pow((.55/lam), self.indexx)
		return t


