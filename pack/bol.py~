"""
A set of classes and functions to analyse the bolometric light curves as computed from Stephane's code

Also a set of generic functions that can be used as per convenience (e.g. ODR line fitting)


"""

from scipy.interpolate import interp1d
from scipy.odr import *

import os
import numpy as np

homept = os.path.expanduser("~")

rn=np.random.normal
class bol_func:
	"""
	Class to store all functions required for evaluating parameters from bolometric light curves (calculated using mklcbol.pro)

	Functions also to calculate the rise from half maximum a la contardo 2000


	"""

	def bolpeak(self, fil):
		"""
		Interpolate to find bolometric peak ##TOADD: exceptions for when the peak is not measured
		
		note: written on top of interp1d from scipy.interpolate (boss function it is!)
		"""
		
		lc=np.loadtxt(fil)
		ter=interp1d(lc[:,0], lc[:,1], kind='cubic')
		l=np.linspace(lc[:,0].min(), lc[:,0].max())
		gpl=ter(l)
	
	
		#e = lc[:,2][abs(lc[:,1] - max(gpl)) == min(abs(lc[:,1] - max(gpl)))][0]
		if max(gpl) != lc[0][1]:
			return max(gpl), l[gpl==max(gpl)][0]#, e 
	
	
		else: 
			return 99.0, 99.0#, 99.0
	
	
	def err_peak(self, arr):
		real=rn(arr[:,1], arr[:,2])
		ph=arr[:,0]	
		
		spl=interp1d(ph, real, kind='cubic')
		l=np.linspace(ph.min(), ph.max())
		
		gpl=spl(l)	
		return max(gpl), l[gpl==min(gpl)][0]
	def precalc_magerr(self, arr, n=10000):
		ar = [err_peak(arr) for k in range(n)]
		ar = np.array(ar)
		
		return np.mean(ar[:,0]), np.std(ar[:,0]) 
		 
	def dm15_bol(self,fil):

		"""

		Delta m 15 for the bolometric light curve 
		"""
		lc1=np.loadtxt(fil)
		
		sp=interp1d(lc1[:,0], lc1[:,1], kind='cubic')
		
		l=np.linspace(min(lc1[:,0]), max(lc1[:,0]), 100)
		
		gp=np.log10(sp(l))
		
		tm=l[gp==max(gp)]
		
		ph=lc1[:,0]-tm
		
		if min(ph)<0 and max(ph)>15:
		
			ph1=abs(l-15)
			m15=gp[ph1==min(ph1)][0]
		
			return max(gp)-m15#np.log10(max(gp))-np.log10(m15)	
		else:
			return 99.0
	def late_decl(self, arr1, ran=[200, 400]):
		"""
		Uses the light curve array (NOT filename)
		"""
		arr=arr1[(arr1[:,0]>ran[0]) & (arr1[:,0]<ran[1])]
		if len(arr)>=4:
			A=np.vstack([arr[:,0], np.ones(len(arr))]).T
			m=np.linalg.lstsq(A, arr[:,1])[0]
			return m
		else:
			return [99.0, 99.0]
class model_comp:

	pt='/home/sdhawan/'; direc='bol_ni_ej/comp_ddc/'
	infile='lpeak_m56ni.dat'
	inp=pt+direc+infile
	def interp_mni(self, val, qtt):
		"""
		Interpolate the peak magnitude of Blondin et al. [2013] DDC models to get a nickel mass.
		the columns are
		Ni Bol BVRI BVRIJH BVRIJHK UBVRI UBVRIJH UBVRIJHKs
		
		"""
		inval=np.loadtxt(self.inp, usecols=(1, qtt))
		lpeak=sorted(inval[:,1]); mni=sorted(inval[:,0])
		spl=interp1d(lpeak, mni, kind='cubic')
		u=np.linspace(min(lpeak), max(lpeak), 500)#; v=np.linspace(mni.min(), mni.max())
		gl=spl(u)
		absl=abs(u-val)	
		nivar=gl[absl==min(absl)]
		return nivar
class mc:
	"""
	Class of MC functions for testing distributions and non-gaussian behaviour
	"""
	def ar_crt(self, n,	t0=[1., 2.]):
		ar=[rn(t0[0], t0[1]) for i in range(n)]
		return ar
	
	def rel_ni(self, mb,n):
		ar=[pow(10, -0.4*(rn(mb[0], mb[1])+rn(19.841, 0.020))) for k in range(n)]
		return ar




class reden:
	
	b14=np.loadtxt(homept+"/bol_ni_ej/burns14_ebv.tex", dtype='string', delimiter='&')
	def b14_av(self, SN):
		bf=self.b14
		row=bf[bf[:,0]==SN+' '][0]
		try:
			
			ebv=float(row[5][2:7])
			
			rv=float(row[7][2:5])
			
			return ebv*rv
		except:
			return "There is no R_v with this method"
	def b14_sbv(self, SN):
		bf=self.b14
		
		try:
			row=bf[bf[:,0]==SN+' '][0]
			ebv=float(row[3][1:6])
			
				
			return ebv
		except:
			return 99.0	#what a failed attempt at trying to amuse yourself

def spl_fit(arr, val):
	"""
	interpolate value for Nickel mass
	"""
	real=rn(arr[:,0], arr[:,1])
	terp=interp1d(real, rn(arr[:,2], arr[:,3]), kind='cubic')
	l=np.linspace(real.min(), real.max())
	gpl=terp(l)
	l1=abs(l-val)
	return gpl[l1==min(l1)][0]
def arn_coef(rt, alp=1):
	"""
	For a given rise time, calculate the coefficient for the relation between Nickel mass and peak bolometric luminosity (arnett's rule, instantaneous energy deposition is output energy at max )
	

	Default alpha is 1 (arguments in Branch+ 1992, stritzinger 2006)
	"""

	eni=6.45e43*np.exp(-rt/8.8)+1.45e43*np.exp(-rt/111.1)

	return alp*eni/1e43

def arn_coef_mc(n, rt=[19, 3], alp=1):
	"""
	n realisations of the coefficient from arnett's rule

	rise time value, default from Stritzinger+

	"""

	ar=[arn_coef(rn(rt[0], rt[1]), alp=1) for k in range(n)]	

	return np.mean(ar), np.std(ar)

def rise_dm15(dm15):
	return 16.5-5*(dm15-1.1)

def rd_bol(sn, pt=homept+'/bol_ni_ej/lcbol_distrib/', suf='_lcbol_u_CSPB_CSPV_CSPr_CSPi_CSPJ_CSPH_CSP.dat'):
	f = np.loadtxt(pt+sn+suf)
	f[:,0] -= bol_func().bolpeak(pt+sn+suf)[1]
	return f, bol_func().bolpeak(pt+sn+suf)
	
def t_half_rise(fil, kind):
	"""
	Calculate the time to rise to max from half the luminosity 
	
	kind: spline, polyfit
	"""
	
	peak=bol_func().bolpeak(fil); tmax=peak[1]
	#load LC
	lc=np.loadtxt(fil)
	#use only the pre-max light curve 
	ph=lc[:,0]-tmax
	ph1=ph[ph<0]; mag1=lc[:,1][ph<0]
	
	if kind == "spline":
		
	
		spl=interp1d(ph1, mag1, kind='cubic')
		l=np.linspace(ph1.min(), ph1.max()); gpl=spl(l)
		arr=abs(gpl-(peak[0]/2.0))
		minval=l[arr==min(arr)][0]
		
		if minval>min(ph):
			return minval
		else:
			return 99.0	

	if kind=="polyfit":
		coef=np.polyfit(ph1, mag1, 2.0)
		lp=np.linspace(-20, 0.0)
		magval=coef[0]*(lp**2)+coef[1]*lp+coef[2]
		mhalf=peak[0]/2.0
		thalf=lp[abs(magval-mhalf)==min(abs(magval-mhalf))]
		
		return thalf
def scal14_ni(x1, n):
	ar=np.array([rn(x1[0], x1[1])*rn(0.100, 0.020)+rn(0.478, 0.023) for k in range(n)])
	return np.mean(ar), np.std(ar)	

def err_comp(lbol, rise, rt=[19, 3],n=10000):
	e = arn_coef_mc(n)[1]
	pk = arn_coef(rt[0])
	if rise:
		ar = np.array([lbol[0]/rn(2, e) for k in range(n) ])	
	else:
		ar = np.array([rn(lbol[0], lbol[1])/pk for k in range(n)])

	return np.mean(ar), np.std(ar)

def err_varrise(lbol, rise, sn, rt=[19, 3],n=10000):

	dmfile = np.loadtxt(homept+'/tests_paper/ni/files_snpy/tmax_dm15.dat', dtype='string')
	dm15 = float(dmfile[dmfile[:,0]==sn][0][3])
	
	vrt = 16.5 + 5*(dm15 -1.1)
	e = arn_coef_mc(n, rt=[vrt, 2.])[1]
	pk = arn_coef(vrt)
	print pk
	if rise:
		ar = np.array([lbol[0]/rn(pk, e) for k in range(n) ])	
	else:
		ar = np.array([rn(lbol[0], lbol[1])/pk for k in range(n)])

	return np.mean(ar), np.std(ar)

"""
def t2lmax(band):
	l=np.loadtxt('out_files/lbolhist_'+band+'.txt', dtype='string')
	if band=='j':
		t2=np.loadtxt('whole_samp.txt', dtype='string')
		slp=[0.04, 0.004]
		inc=[0.04, 0.118]
	else:
		t2=np.loadtxt('/home/sdhawan/tests_paper/')
	t2arr=np.array([[float(i[1]), float(i[2])] for i in t2 if i[0][2:] in l[:,0]])


def newlmax(filt):
	y=np.loadtxt('out_files/lbolhist_'+filt+'.txt', dtype='string')
	if filt == 'y':
		m=(y[:,1].astype('float32')+0.05
		vs=np.vstack([y[:,0], m, y[:,2]]).T
		np.savetxt('out_files/lbol')
	elif filt == 'j':
"""
class linfits:
	def freq_odr(self, arr):
		"""
		scipy.odr, best fit line
		"""
		rd=RealData(arr[:,0], arr[:,2], sx=arr[:,1], sy=arr[:,3])
		def f(B, x):
			return B[0]*x+B[1]
		f=Model(f)
		od=ODR(rd, f, beta0=[1., 2.])
		out=od.run()
		return out.beta, out.sd_beta
	def freq_noerr_linalg(self, arr):
		A=np.vstack([arr[:,0], np.ones(len(arr))]).T
		m,c=np.linalg.lstsq(A, arr[:,1])[0]
		return m, c
	def freq_noerr(self, arr):
		rd=RealData(arr[:,0], arr[:,1])
		def f(B, x):
			return B[0]*x+B[1]
		f=Model(f)
		od=ODR(rd, f, beta0=[1., 2.])
		out=od.run()
		return out.beta, out.sd_beta
	def freq_yerr(self, arr):
		rd=RealData(arr[:,0], arr[:,1], sy=arr[:,2])
		def f(B, x):
			return B[0]*x+B[1]
		f=Model(f)
		od=ODR(rd, f, beta0=[1., 2.])
		out=od.run()
		return out.beta, out.sd_beta		





