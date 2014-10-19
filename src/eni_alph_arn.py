#loads the bolometric peak values and calculates the ni masses for a variable rise time
#options to modify alpha.
import mag2fl as mf
import numpy as np			# imports to use basic numpy libraries
import matplotlib.pyplot as plt

import sys

from scipy.stats import pearsonr
from scipy.odr import *
bd=sys.argv[2]
class alp_cons:			# class to define all files and arrays for the effect of rise time on the Ni mass measurements
	lp=np.loadtxt('lpeak_m56ni.dat', usecols=(1, 3, 4, 7))		#load the DDC model values for comparison
	dm=np.loadtxt('/home/sdhawan/tests_paper/ni/files_snpy/tmax_dm15.dat', dtype='string')	# load dm15 for the rise calculation
	t=np.loadtxt('/home/sdhawan/tests_paper/csp_sn/sec_max_files/'+bd+'_sec_max_csp.dat', dtype='string')	#load t2
	ub=np.loadtxt('tables/tab2_pap.txt', dtype='string', skiprows=1)
	ub=ub[ub[:,4]=='UBVRIJH']					#load ni/lbol
	darr=np.array([float(dm[dm[:,0]==i[0]][0][3]) for i in ub if i[0] in dm[:,0] and i[0] in t[:,0]])	#array of Dm15 values for the objects in the 
	tarr=np.array([float(t[t[:,0]==i[0]][0][1]) for i in ub if i[0] in dm[:,0] and i[0] in t[:,0]])		#the t2 arr
	etarr=np.array([float(t[t[:,0]==i[0]][0][2]) for i in ub if i[0] in dm[:,0] and i[0] in t[:,0]])	
	ssub=np.array([[i[0], float(i[1]), float(i[2])] for i in ub if i[0] in dm[:,0] and i[0] in t[:,0]])
	alp=1														# alpha=1, this parameter measures the deviation from arnett's rule, Scalzo '14 uses 1.2 +/- 0.2
	#alp=float(sys.argv[2])
	tr=17.5-5*(darr-1.1)-1#+tbarr#float(sys.argv[1])				#Ganeshalingam+'11, Scalzo '14
	eni=6.45e43*np.exp(-tr/8.8)+1.45e43*np.exp(-tr/111.3)	#arnett's rule as a function of rise, eqn from stritzinger '05
	lmax=alp*eni/1e43			#constant value to map lmax to mni 
	newn=ssub[:,2].astype('float32')/lmax		#Ni mass with varying rise time for Arnett's rule 
	ns=zip(ssub, newn)
	def f(self, B, x):
		return B[0]*x+B[1]
		
	#np.savetxt('arn_dev/tr_var_mni.dat', ns, fmt='%s')
ap=alp_cons
#print np.mean(ap().lmax), np.std(ap().lmax), np.std(ap().tr), pearsonr(ap().tarr, ap().lmax)	
if int(sys.argv[1])==1:
	ll=ap().ssub[:,1].astype('float32')		#Ni masses from the peak bolometric luminosity 		# which array (i.e. set of values of Mni do you want to use for testing the correlations)
elif int(sys.argv[1])==2:
	ll=ap().newn			# array of non-linear Ni values i.e. the arnett's rule relation is dependent on tR, which is a function of t2/dm15
else:	
	ll=ap().ssub[:,2].astype('float32')#/2		#peak bolometric luminosity

rd=RealData(ap().tarr, ll, sx=ap().etarr, sy=ll/10)
f1=Model(ap().f)
out=ODR(rd, f1, beta0=[1., 2.])
o=out.run()
print  np.mean(ap().tr)#pearsonr(ap().tarr, ll), len(ll) #len(ap().newn)  o.beta, o.sd_beta,
plt.scatter(ap().tarr, ll)
plt.show()
