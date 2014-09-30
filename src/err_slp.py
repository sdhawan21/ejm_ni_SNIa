import numpy as np
import matplotlib.pyplot as plt
import sys

from scipy.interpolate import interp1d
from scipy.odr import *
from scipy.stats import pearsonr
pt='/home/sdhawan/tests_paper/csp_sn/sec_max_files/'


band=sys.argv[1]
t=float(sys.argv[2])
et=float(sys.argv[3])

print band
ufl=np.loadtxt('../tables/u_flags.txt', dtype='string', skiprows=1)
tj=np.loadtxt(pt+band+'_sec_max_csp.dat', dtype='string')

def lbol_red(tval):
	lb=np.array([float(i[1]) for i in ufl if i[0] in tj[:,0]])
	elb=np.array([float(i[2]) for i in ufl if i[0] in tj[:,0]]) 
	t2=np.array([float(tj[tj[:,0]==i[0]][0][1]) for i in ufl if i[0] in tj[:,0]])
	et2=np.array([float(tj[tj[:,0]==i[0]][0][2]) for i in ufl if i[0] in tj[:,0]])
	nsamp=100
	rd=RealData(t2, lb, sx=et2, sy=elb)
	def f(B,x):
		return B[0]*x+B[1]
	f=Model(f)
	out=ODR(rd, f, beta0=[1., 2.])
	o=out.run()
	val=o.beta
	err=o.sd_beta
	print len(t2), err, val
	ar=[np.random.normal(val[0], err[0])*np.random.normal(tval[0], tval[1])+np.random.normal(val[1], err[1]) for i in range(1000)]
	return np.array(ar)
def coeff(dm15):
	rt=17.5-5*(dm15-1.1)
	lm=6.45e43*np.exp(-rt/8.8)+1.45e43*np.exp(-rt/111.1)
	return lm/1e43
def main():
	v=t
	ev=et                              
	ar=lbol_red([v, ev])
	print np.mean(ar)/2,(np.mean(ar)/2)*((0.3/2.0)+(ev/v))
	plt.hist(ar)
	#plt.show()
main()