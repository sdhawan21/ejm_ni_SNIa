"""
Plot an error comparison between the values we obtain from the fits and the values from richard's mcmc

"""

import numpy as np
import matplotlib.pyplot as plt

#load richard's estimates
rc=np.loadtxt('s14_files/snmcmc_results_runBp_mlo.txt', usecols=(16, 19, 17, 20))

#load the Dm15 values 
dm=np.loadtxt('tmax_dm15.dat', dtype='string')

#class of functions to give out error estimates and dm15 values 
class der_ni:		
	vals=np.loadtxt('tables/u_flags.txt', usecols=(1, 2), skiprows=1)#, dtype='string')
	nm=np.loadtxt('tables/u_flags.txt', dtype='string', skiprows=1)[:,0]	
	def div_err(self,x, y, dx, dy):
		"""
		error values for  a division 
		"""
		err=(dx/y)-((x*dy)/(y**2))
		e1=(dx/x)**2+(dy/y)**2
		return np.sqrt(e1)*(x/y)
	def mc(i):
		e=self.err
		arr=[np.random.normal(i[0], i[1]) for k in range(1000)]
		return np.mean(arr), np.std(arr)
	def cons(self):
		dm1=np.array([17.5-5*(float(dm[dm[:,0]==ll][0][3])-1.1) for ll in self.nm if ll in dm[:,0]])
		return dm1
	def subarr(self):
		v1=np.array([])
		return v1
def main():
	v=der_ni().vals		
	
	#comparison of error estimates from Ni-Richard measured with the errors from fixed and variable rise times in our calculations 
	
	nm=der_ni().nm
	
	v1=[[float(v[nm==ll][0][0]), float(v[nm==ll][0][1])] for ll in nm if ll in dm[:,0]]; v1=np.array(v1)
	cn=der_ni().cons()
	
	er=6.45*np.exp(-cn/8.8)+1.45*np.exp(-cn/111.3) 		#expression from stritzinger '06
	
	#assert the vector lengths
	assert len(cn)==len(v1)
	
	fina=np.array([[v1[i][0]/2.0, der_ni().div_err(v1[i][0], er[i], v1[i][1], 0.3)] for i in range(len(v1))])
	plt.hist(fina[:,1], alpha=0.3, color='b')
	plt.hist(rc[:,3], alpha=0.3, color='g')
	plt.show()
	#print fina
main()
