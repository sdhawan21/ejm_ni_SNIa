import numpy as np
import matplotlib.pyplot as plt
import sys

from scipy.interpolate import interp1d

pt='/home/sdhawan/tests_paper/csp_sn/sec_max_files/'

ufl=np.loadtxt('../tables/u_flags.txt', dtype='string')
tj=np.loadtxt(pt+'j_sec_max_csp.dat', dtype='string')
def lbol_red(tval):
	lb=np.array([float(i[1]) for i in ufl if i[0] in tj[:,0]])
	elb=np.array([float(i[2]) for i in ufl if i[0] in tj[:,0]]) 
	t2=np.array([float(tj[tj[:,0]==i[0]][0][1]) for i in ufl if i[0] in tj[:,0]])
	et2=np.array([float(tj[tj[:,0]==i[0]][0][2]) for i in ufl if i[0] in tj[:,0]])
	nsamp=100
	
	lb_array=[]
	
	for i in range(nsamp):
		real_t2=np.random.normal(t2, et2)
		real_lb=np.random.normal(lb, elb)
		kk=interp1d(real_t2, real_lb, kind='cubic')
		ll=np.linspace(real_t2.min(), real_t2.max())
		spl=kk(ll)
		l1=abs(ll-tval)
		l=spl[l1==min(l1)]
	
		lb_array.append(l)
	return lb_array

def main():
	arr=lbol_red(28.37)
	print np.mean(arr)
main()
