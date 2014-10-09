#calculate fiducial time for a given SN and Nickel mass

import numpy as np
import sys
import matplotlib.pyplot as plt

from astropy.modeling import fitting, models
from scipy.interpolate import interp1d
from scipy.optimize import leastsq, curve_fit
#from bol_lc import bol_cl, lpeak_ni


#number of seconds in a day
ds2=86400.0
#e-fold times for nickel and cobalt (56, resp.)			
lni=1/(8.8)
lco=1/(111.3)		

#Mev to ergs
fac=624150.647996		

#input SN from command line
obj=sys.argv[1]

#some sort of scale factor
sc=1e10

#array of times 
tarr=np.linspace(50, 100, 100)


class mej:
	"""
	defined the class for the required functions
	"""
	
	def edp(self,  t, Nni, t0):
		"""
		function for energy deposition; equation in Nadyozhin 1994
		"""
		#ENi
		t1=lni*Nni*np.exp(-lni*t)*(1.75)		
		#ECo_e+
		t2=lco*Nni*(lni/(lni-lco))*(np.exp(-lco*t)-np.exp(-lni*t))	
		#ECo_gamma
		t3=(0.12)+(3.61)*(1-np.exp(-(t0/t)**2))		
		return (t1+t2*t3)/(fac*ds2)#(t2*t3)/(fac*ds2)
	
	
	def rd_lc(self, sn, bands):
		"""
		read in bolometric lc
		"""
		return np.loadtxt('lcbol_distrib/'+sn+'_lcbol_'+bands+'.dat')
		
	def numb(self, mni):
		"""
		converts the nickel mass to number of nickel nuclei (precision checked, no overflow errors here)
		"""
		return mni*1.98e33*6.022e23/56.0
		
	def p2ni(self, sn, bands):
		"""
		function to calculate the Ni mass when input isnt given. Cubic spline interpolation to the peak
		"""
		t=self.rd_lc(sn, bands)
		r1=np.random.normal(t[:,1], t[:,2])
		p=interp1d(t[:,0], r1, kind='cubic')
		o=np.linspace(min(t[:,0]), max(t[:,0]), 100)
		u=p(o)
		return o[u==max(u)], max(u) 
		
	def ran(self, arr1, arr2):
		"""
		generic function to define the range for selection in an array
		"""

		return arr1[(arr1>=40) & (arr1<=100)], arr2[(arr1>=40) & (arr1<=100)]
	def slp(self, arr1, arr2):
		"""
		least squares fit for late decline rate (no errors)
		
		TODO: errors, ODR/statsmodels implementations
		"""
		a=np.vstack([arr1, np.ones(len(arr1))]).T
		return np.linalg.lstsq(a, arr2)[0]
		
#input nickel mass (nim)
nim=float(sys.argv[2])#mej().p2ni(obj,'BVRIJH')[1]/2e43
#print nim

#define the set of bands using which the bolometric light curve has been calculated 
#note: for our sample UBVRIJH since we've selected as such
bands=sys.argv[3]

#input distance
dm=float(sys.argv[4])

#rise time calculation from the Dm15 input
rt=17.5-5*(dm-1.1)

#read in the bolometric light curve 
lcbol=mej().rd_lc(obj, bands)

#shift time axis wrt bolometric peak
ph=lcbol[:,0]-mej().p2ni(obj,bands)[0]

#print ph
#lcbol[:,1]*=8.6e25**2

l1=np.linspace(0, 50, 100)
l2=np.linspace(-20, 100, 100)

#late decline region of LC
ph1,mag1=mej().ran(ph, lcbol[:,1])
#slope of log flux (2.5 factor not applied)
m=mej().slp(ph1, np.log10(mag1))

ed=m[0]*ph1+m[1]
func=mej().edp
#print leastsq(func, mag1, args=(mej().numb(nim)))
edarr=[sum((mej().edp(ph1, mej().numb(nim), i)-mag1)**2) for i in l1]
edarr=np.array(edarr)
#plt.plot(l2,  np.log10(mej().edp(l2, mej().numb(nim), 10))-.32)
#plt.plot(l2,  np.log10(mej().edp(l2, mej().numb(nim), 1e7))-.32)
plt.plot(ph, np.log10(lcbol[:,1]), 'r.')
t0=l1[abs(edarr)==min(abs(edarr))]+rt
ejm=8*np.pi*(((t0)*ds2)**2)*9e6*sc*3/(0.025*1.98e33)		#eq 4. Stritzinger '06  (akin to eqn 4 Scalzo 2014)
plt.plot(ph-rt,  np.log10(mej().edp(ph,  mej().numb(nim), t0[0])))
plt.show()
fout=open('fast_decl/fdecl_ejm_recon.txt', 'a')
fout.write(sys.argv[1]+'\t'+str(ejm[0])+'\n')
#fout.write('SN'+obj[2:len(obj)]+'\t'+str(ejm[0])+'\t'+str(dm)+'\n')
print    t0[0], ejm[0] #print out the values for the total ejecta mass and the transparency time

#print ph, mej().edp(55.0, mej().numb(0.38), 32.16)/fac
