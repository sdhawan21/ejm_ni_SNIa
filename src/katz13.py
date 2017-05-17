#using equation 1 of Katz et al. to measure Nickel mass

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import simps,quad
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
#from pack import bol
from bol import bol_func

bp = bol_func().bolpeak

class q_func:
	
	qco_e = 0.12
	qco_g = 3.61
	
	qni = 1.75
	
	tni = 8.8
	tco = 111.1
	
	fac=624150.647996
		
	ds2=86400.0
	
	def mni(self,t):
		return np.exp(-t/self.tni)

	def mco(self,t): 
		return (np.exp(-t/self.tco)-np.exp(-t/self.tni))*self.tco/(self.tco - self.tni)
		
	def qtot(self,t):
	
		niterm=self.qni * self.mni(t)/self.tni
		
		coterm = (self.qco_e + self.qco_g) * self.mco(t)/self.tco
		
		return (niterm+coterm)/(self.fac*self.ds2)
	
	def edp(self,  t):
		"""
		function for energy deposition; equation in Nadyozhin 1994
		"""
		
		lni=(1/8.8)
		
		lco=(1/111.1)
		
		fac=624150.647996
		
		ds2=86400.0
		
		#ENi
		t1=lni*np.exp(-lni*t)*(1.75)		
		#ECo_e+
		t2=lco*(lni/(lni-lco))*(np.exp(-lco*t)-np.exp(-lni*t))	
		#ECo_gamma
		t3=(0.12)+(3.61)#*(1-np.exp(-(t0/t)**2))		
		return t*(t1+t2*t3)/(fac*ds2)#(t2*t3)/(fac*ds2)
	
	
def shift_phase(sn):
        if sn == 'SN2002dj':
                f = '../lcbol_distrib/'+sn+'_lcbol_U_AstierB_CSPV_CSPr_CSPi_CSPJ_CSPH_CSP.dat'
        elif sn == 'SN2002fk':
                f = '../lcbol_distrib/'+sn+'_lcbol_u\'B_CSPV_CSPr_CSPi_CSPJ_CSPH_CSP.dat'
        elif sn == 'SN2011fe':
                f = '../lcbol_distrib/'+sn+'_lcbol_UBVRI.dat'
        else:
                f = '../lcbol_distrib/'+sn+'_lcbol_u_CSPB_CSPV_CSPr_CSPi_CSPJ_CSPH_CSP.dat'
	
	lc = np.loadtxt(f)
	
	b = bp(f)[1]
	
	lc[:,0]-=b
	#lc[:,0]=15
	return lc
	
def mass(nni):

	return nni*56.0/(1.98e33*6.022e23)	
	
def fl_int(sn,ph = [10, 40]):
	
	a1 = shift_phase(sn)
	arr = a1[(a1[:,0]>ph[0]) & (a1[:,0] < ph[1])]
	
	arr[:,1]*=arr[:,0]
	#integrate the bolometric 
	s = simps(arr[:,1]*arr[:,0], arr[:,0])
	
	return s
	
def qfunc(t):
        a=np.exp(-t/8.8) 
	b = np.exp(-t/111.1) - np.exp(-t/8.8)	
        return (1.75*a/8.8) + (3.73*b/102.3)
def int_denom(t):
	return t*qfunc(t)
	
def rise_fit(arr, firstobs):
        #fit polynomial to early time (pre-max) data
	a = np.polyfit(arr[:,0], arr[:,1], 2)
	t_axis = np.linspace(firstobs, 0)
	return a[0]*t_axis**2 + a[1]*t_axis + a[2]
	
def main():
	
        sn = sys.argv[1]

        #dm15_file = np.loadtxt('/Users/lapguest/all_paper/files_snpy/tmax_dm15.dat', dtype='string')

        #dm = float(dm15_file[dm15_file[:,0]==sn][0][3])

        fout = open('../out_files/katz_nimass.dat', 'a')
	#Mev to erg/s
	fac=624150.647996
	
        #maximum post-peak phase
        phmax = 30
	
	#days to seconds 
	ds2=86400.0
	
        #phased light curve
	lc = shift_phase(sn)
	
        #spline interpolation of the bolometric light curve
	l = np.linspace(lc[:,0].min(), lc[:,0].max())
	spl = interp1d(lc[:,0], lc[:,1], kind='cubic')
	gp = spl(l)

	
       

        #condition for post-maximum data

	cond =  (0 < l) & (l < phmax)
        
        #tr = 16.5 - 5*(dm-1.1)
        firstobs = -19
        print firstobs
	premax = l < 0
	

         #integrate the energy decay function
	q_int = quad(qfunc, firstobs, phmax)[0]

        # pre-max data for parabola fit
	vs = np.vstack([l[premax], gp[premax]]).T
	
        #fit the rise 
	polyfit = rise_fit(vs, firstobs)
	#pre-max time array
	t_axis = np.linspace(firstobs, 0)

	gp *=l
        #integral from post-max
	s = simps(gp[cond], l[cond])
	
        #integral from pre-max
	s1 = simps(polyfit*t_axis, t_axis)
	
        #number of Ni nuclei (ratio of the integrals and conversion factors)
	nni= (s+s1)*fac*ds2/(q_int)


	
	print mass(nni)
	
        fout.write(sn +'\t'+ str(mass(nni))+'\n')
        fout.close()

        #plot the results
        plt.plot(lc[:,0], lc[:,1], 'ro')
#	plt.plot(l[cond], gp[cond])
        plt.plot(t_axis, polyfit)
	plt.plot(lc[:,0], qfunc(lc[:,0])*nni/(fac*ds2))
	plt.show()


	return 0

	print "The minimum phase for this SN is:", min(lc[:,0])
	rhs = fl_int(sn, ph = [min(lc[:,0]), 20])
	
	edec = q_func().qtot
	
	p=np.linspace(10, 40)
	e = q_func().edp(p)
	

	
	
	lhs=quad(q_func().edp, min(lc[:,0]), 20)[0]
#	lhs = simps(e, p)
	
	
	print mass(rhs/lhs)

	plt.fill_between(p, 0)
	plt.plot(lc[:,0], lc[:,1]*lc[:,0])
	plt.plot(p, e*1.98e33*6.022e23/56.0)
	plt.show()

main()


