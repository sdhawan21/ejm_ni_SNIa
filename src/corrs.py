import numpy as np
import matplotlib.pyplot as plt
import sys


from scipy.odr import *
class dec:
	def f(self, B, x):
		return B[0]*x+B[1]
	def lt_dec(self):
		rd=RealData(t2, mm, sx=et, sy=em)
		f=Model(self.f)
		od=ODR(rd, f, beta0=[1., 2.])
		out=od.run()
		return out.beta, out.sd_beta
if len(sys.argv)<6:
	print "define the band for t2, whether the ejecta or nickel mass is being used and whether you want to see the correlation with the decline rate"
	print "Usage: python"+sys.argv[0]+"\t <ni file> <ejm file> <band> <ejm/dm15> <param to corr with>"


bd=sys.argv[3]
from scipy.stats import pearsonr

pt='../tests_paper/csp_sn/sec_max_files/'+bd+'_sec_max_csp.dat'
pt1='../tests_paper/ni/files_snpy/tmax_dm15.dat'
mni=np.loadtxt(sys.argv[1]+'.txt', dtype='string',  skiprows=int(sys.argv[6]))
ej=np.loadtxt(sys.argv[2]+'.txt', dtype='string')
t=np.loadtxt(pt, dtype='string')
dm=np.loadtxt(pt1, dtype='string', usecols=(0, 3, 4))
rs=np.loadtxt('s14_files/snmcmc_results_runBp_mlo.txt', dtype='string', usecols=(0, 16, 19, 1))
if sys.argv[4]=='0':
	t=ej
elif sys.argv[4]=='1':
	t=dm
if sys.argv[5]=='ej':
	mni=ej
elif sys.argv[5]=='sc':
	mni=rs
sc14=np.loadtxt('s14_files/sc14_ejni.txt', usecols=(1, 2))

t2=[float(i[1]) for i in t if   i[0] in mni[:,0]]
et=[float(i[2]) for i in t if   i[0] in mni[:,0]]
#ni=[float(rs[rs[:,0]==i[0]][0][19]) for i in t if i[0] in mni[:,0]]
mm=[float(mni[mni[:,0]==i[0]][0][1]) for i in t if  i[0] in mni[:,0] ]
em=[float(mni[mni[:,0]==i[0]][0][1]) for i in t if  i[0] in mni[:,0] ]
#plt.plot(t2, ni, 'ro')
plt.plot(t2, mm, 'b^', label='this work')
#plt.plot(sc14[:,0], sc14[:,1], 'gp', alpha=0.3, label='Scalzo 14')
#plt.plot(rs[:,1], rs[:,2], 'yD', alpha=0.3, label='RS MCMC file')
#plt.plot(2.18, 1.55,'ko', label='SN2007if')
#plt.legend(loc=2)
#plt.xlabel('$M_{ej}$')
#plt.ylabel('$M_{Ni}$')
plt.show()
a=np.vstack([t2, np.ones(len(t2))]).T
sl=np.linalg.lstsq(a, mm)[0]
t2=np.array(t2);# ni=np.array(ni)
a=np.vstack([t2, np.ones(len(t2))]).T
b=np.linalg.lstsq(a, mm)[0]
r=dec().lt_dec()
arr=np.array([np.random.normal(r[0][0], r[1][0])*np.random.normal(25.10, 0.22)+ np.random.normal(r[0][1], r[1][1]) for i in range(1000)])
print "pearsonr and p values for \t" +sys.argv[3]+'band:\t', pearsonr(mm,t2), 
print 'scatter and mni 14J are \t',  np.std(mm-sl[0]*t2-sl[1]),  b[0]*28.37+b[1] #, np.std(mm), len(t2[t2>1.3]), dec().lt_dec(), np.mean(arr), np.std(arr) #b[0]*28.37+b[1]
