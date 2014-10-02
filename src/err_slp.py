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
y2j=np.loadtxt('../y2j.txt', dtype='string')
rn=np.random.normal
def lbol_red(tval):
	
	#define arrays for x, y, ex, ey (not in that order)
	lb2=np.array([float(i[1]) for i in ufl if i[0] in tj[:,0]])
	elb2=np.array([float(i[2]) for i in ufl if i[0] in tj[:,0]]) 
	jt2=np.array([float(tj[tj[:,0]==i[0]][0][1]) for i in ufl if i[0] in tj[:,0]])
	jet2=np.array([float(tj[tj[:,0]==i[0]][0][2]) for i in ufl if i[0] in tj[:,0]])
	
	#array for the y2j conversion (if specified by command line)
	if int(sys.argv[4])==1:
		lb1=np.array([float(i[1]) for i in ufl if i[0] in tj[:,0]])
		elb1=np.array([float(i[2]) for i in ufl if i[0] in tj[:,0]]) 
		yt2=np.array([float(tj[tj[:,0]==i[0]][0][1]) for i in ufl if i[0] in tj[:,0]])
		yet2=np.array([float(tj[tj[:,0]==i[0]][0][2]) for i in ufl if i[0] in tj[:,0]])
	
		lb=np.concatenate([lb1, lb2]); elb=np.concatenate([elb1, elb2]); t2=np.concatenate([jt2, yt2])
		et2=np.concatenate([jet2, yet2])
	
	else:
		lb=lb2; elb=elb2; t2=jt2; et2=jet2
		
	#define Nsamp
	nsamp=100
	#perform least-squares
	rd=RealData(t2, lb, sx=et2, sy=elb)
	def f(B,x):
		return B[0]*x+B[1]
	f=Model(f)
	out=ODR(rd, f, beta0=[1., 2.])
	o=out.run()
	val=o.beta
	err=o.sd_beta
	print len(t2), err, val
	#do monte carlo for Mni
	ar=[(np.random.normal(val[0], err[0])*np.random.normal(tval[0], tval[1])+np.random.normal(val[1], err[1]))/rn(1.99, 0.31) for i in range(3000)]

	mx=val[0]*tval[0]; c=val[1]
	return ar#mx+c, mx*((tval[1]/tval[0])+(err[0]/val[0])+err[1]), #np.array(ar)


def coeff(dm15):
	rt=17.5-5*(dm15-1.1)
	lm=6.45e43*np.exp(-rt/8.8)+1.45e43*np.exp(-rt/111.1)
	return lm/1e43
def main():
	v=t
	ev=et                              
	ar=lbol_red([v, ev])
	print np.mean(ar), np.std(ar)#, min(ar), max(ar)#np.mean(ar)/2, (np.mean(ar)/2)*((np.std(ar)/np.mean(ar))+(0.3/2.0))
	#(ar[0]/2.0)*((ar[1]/ar[0])+(0.3/2.0))
	#plt.hist(ar)
	#plt.show()
main()
