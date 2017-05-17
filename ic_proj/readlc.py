from numpy import log10, loadtxt, linspace, delete, array, pi, trapz, vstack, ones, linalg
from pandas import *
from matplotlib.pyplot import show, plot
from scipy.interpolate import interp1d
from scipy.stats import pearsonr

import math
import sys
import pickle as pc
h='/home/sdhawan/pap_files/CSP_Photometry_DR2/'		#directory where Lc's are stored
tl='opt+nir_photo.dat'
#disf=loadtxt('/home/sdhawan/csp_dist.txt', dtype='string')
#decl=loadtxt('../tests_paper/ni/files_snpy/tmax_dm15.dat', dtype='string')
#filt=sys.argv[2]
#zp=6.322e-11
#wsset=loadtxt('../tests_paper/csp_sn/sec_max_files/y_sec_max_csp.dat', dtype='string')
#tmax=loadtxt('/home/sdhawan/tests_paper/ni/files_snpy/tmax_dm15.dat', dtype='string')
#pt='/home/sdhawan/bol_ni_ej/s14_files/'
#pt1='/home/sdhawan/tests_paper/csp_sn/sec_max_files/'
class conv:					#class reads in the dat file and stores it as a python dictionary. the second function							#converts dicts to a panel after converting them to dataframes
	def rd_lc(self, sn, band):				#function of use to read the text files in the CSP DR2 directory. 
		f=open(h+sn+tl, 'r')
		f1=loadtxt(h+sn+tl, skiprows=5)
		ls=[]
		for row in f:
			ls.append(row.split())
		ind=ls[4].index(band)
		lc={}
		lc['MJD']=f1[:,0][f1[:,ind]<90]
		lc[band]=f1[:,ind-1][f1[:,ind]<90]
		lc['e_'+band]=f1[:,ind][f1[:,ind]<90]			#read the lc in the given band with the values not equal to 99
		return lc
	def f_ord(self, sn):
		e=open(h+sn+tl, 'r')
		ls=[]
		for row in e:
			ls.append(row.split())
		ind=ls[4].index(ls[4][3])
		s=array(ls[4])
		aub=s[(s != s[3]) & (s !='MJD') & (s!='#')]
		return aub
		
	def df_crt(self, sn,bands):
		data={}
		for i in bands:
			data[i]=DataFrame(self.rd_lc(sn, i))
		pn=Panel(data)
		return pn
#	def rd_col(self, sn):
#		cc=pc.load(open('/home/sdhawan/col_rise/col_curve_csp.txt', "rb"))
		#return cc[sn]


class spl_fit:
	def rd_cfa(self, sn, band):
		pt='/home/sdhawan/bol_ni_ej/vel_decl/cfa_lc/'
		lc=pc.load(open(pt+sn+'_lc.txt', "rb"))
		bb={}
		bb['ph']=lc['ph'+band]
		bb[band]=lc[band]
		return bb
	def bdmax(self, sn, band, sur):				#spline fit to light curve to get max. Only in  cases where the maximum has been sampled, else return 'blank'
		if sur=='cfa':
			lc1=self.rd_cfa(sn, band)
		else:
			lc1=conv().rd_lc(sn, band)
		spl=interp1d(lc1['MJD'], lc1['B'], kind='cubic')
		l1=np.linspace(min(lc1['MJD']), max(lc1['MJD']), 100)
	 examples of LC	gpl=spl(l1)
		tm=l1[gpl==min(gpl)][0]
		if min(lc1['MJD']-tm)<0:
			return min(gpl), l1[gpl==min(gpl)][0]
		else:
			return 99.0, 99.0
	def lt_dec(self, sn, band, sur):
		lc1=self.rd_cfa(sn, band)
		#tm=self.bdmax(sn, band, sur)[1]
		ph=lc1['ph']
		ph1=ph[(ph>=40) & (ph<=90)]
		mag=lc1[band][(ph>=40) & (ph<=90)]
		a=np.vstack([ph1, np.ones(len(ph1))]).T
		m=np.linalg.lstsq(a, mag)[0]
		return m

'''

class m2f:
	def dm(self, sn):
		return float(disf[disf[:,0]==sn][0][1])
	def spl_fit(self, sn, band):
		lc1=conv().rd_lc(sn, band)
		mjd=lc1['MJD']
		b=lc1[band]
		l=linspace(min(mjd), max(mjd), 100)
		sp=interp1d(mjd, b, kind='cubic')
	 examples of LC	gp=sp(l)
		return l[gp==min(gp)], min(gp)
	def mag2f(self, obj, filt):				
		tm, mm=self.spl_fit(obj,filt)
		wv=wvarr[bands==filt]
		print obj
		absm=mm-self.dm(obj)
		zp=zparr[bands==filt]
		apfl=wv*zp*pow(10, mm/2.5)*1e-9
		dist=self.dm(obj)#pow(10, (self.dm(obj)-25)/5.0)*3.08e18
		lbol=apfl*4*pi*(dist**2)
		#lbol=pow(10, (5.48-absm)/2.5)
		return lbol, absm
	def slp(self, arr1, arr2):
		arr3=arr1[(arr1>40) & (arr1<90)]
		arr4=arr2[(arr1>40) & (arr1<90)]
		a=vstack([arr3, ones(len(arr4))]).T
		m=linalg.lstsq(a, arr4)[0]
		return m
	#def trap(self, snar, wvarr):
		#return (sum(snar)*2-snar[0])*(wvarr[-1]-wvarr[0])/4.0
class spl_fit:
	def rd_cfa(self, sn, band):
		pt='/home/sdhawan/bol_ni_ej/vel_decl/cfa_lc/'
		lc=pc.load(open(pt+sn+'_lc.txt', "rb"))
		bb={}
		bb['ph']=lc['ph'+band]
		bb[band]=lc[band]
		return bb
	def bdmax(self, sn, band, sur):				#spline fit to light curve to get max. Only in  cases where the maximum has been sampled, else return 'blank'
		if sur=='cfa':
			lc1=self.rd_cfa(sn, band)
		else:
			lc1=conv().rd_lc(sn, band)
		spl=interp1d(lc1['MJD'], lc1['B'], kind='cubic')
		l1=np.linspace(min(lc1['MJD']), max(lc1['MJD']), 100)
	 examples of LC	gpl=spl(l1)
		tm=l1[gpl==min(gpl)][0]
		if min(lc1['MJD']-tm)<0:
			return min(gpl), l1[gpl==min(gpl)][0]
		else:
			return 99.0, 99.0
	def lt_dec(self, sn, band, sur):
		lc1=self.rd_cfa(sn, band)
		#tm=self.bdmax(sn, band, sur)[1]
		ph=lc1['ph']
		ph1=ph[(ph>=40) & (ph<=90)]
		mag=lc1[band][(ph>=40) & (ph<=90)]
		a=np.vstack([ph1, np.ones(len(ph1))]).T
		m=np.linalg.lstsq(a, mag)[0]
		return m
class rdbol:
	pt='/home/sdhawan/bol_ni_ej/'
	b14=np.loadtxt(pt+'sub_b14_red.txt', dtype='string')	
	def fread(self, sn):
		fout=open(self.pt+'ybollc/'+sn+'_lc_bol.dat','r')
		ls=[]
		for row in fout:
			ls.append(row.split())
		ebv=float(ls[2][1])/float(ls[3][1])
		b14=self.b14
		e14=b14[b14[:,0]==sn[2:len(sn)]][0][1][2:6]
		return ebv, e14
class t2corr:
	r=np.loadtxt(pt+'snmcmc_results_runBp_mlo.txt', dtype='string')
	def rcorr(self, band):
		l=self.r
		t=np.loadtxt(pt1+band+'_sec_max_csp.dat', dtype='string')
		ar1=[float(i[1]) for i in t if i[0] in l[:,0]]
	 examples of LC	ar2=[float(l[l[:,0]==i[0]][0][19]) for i in t if i[0] in l[:,0]]
		return ar1, ar2
class interp:
	pt='/home/sdhawan/bol_ni_ej/'
	lp=np.loadtxt(pt+'lpeak_m56ni.dat', usecols=(1, 3, 4, 7))
	def filt_conv(self):
		l=self.lp
		l1=np.loadtxt(self.pt+'mni_lcbol.txt', dtype='string', skiprows=1)
		#l1=l1[l1[:,5]==bands]
		#if bands=='BVRIJH':
	#		ind=2
	#	else:
	#		ind=1	
		arr=[]
		for j in l1:
			i=float(j[4])
			if j[5]=='BVRIJH':
				ind=2; fac=1
			else:
				ind=1; fac=1
			ter=interp1d(l[:,ind], l[:,3], kind='cubic')
			ll=np.linspace(min(l[:,ind]), max(l[:,ind]), 100)
			gp=ter(ll)
			g2=gp[abs(ll-i)==min(abs(ll-i))]
			arr.append(g2[0]*fac)
		arr=np.array(arr)
		fin=zip(l1[:,0], l1[:,1], arr, arr/2)
		#aa=np.shape(l1)
		#ts=np.zeros([aa[0], aa[1]+1])
		#ts[:, :-1]=l1
		#ts[:,-1]=arr
		return np.savetxt('uband_mni.txt',fin, fmt='%s')
		#c1=l1[:,3].astype('float32')
		#c2=l1[:,4]
	 examples of LC	#sset=l[c2==bands]
		#s2=l[c2=='BVRIJH']
print interp().filt_conv()
	#pearsonr(ar1, ar2)		
#print rdbol().fread('SN2007as')



'''





















'''	
ar=[]
ar1=[]
for obj in wsset[:,0]:
	try:
		lc1=conv().rd_lc(obj, 'Y')
		ph=lc1['MJD']-float(tmax[tmax[:,0]==obj][0][1])
		t2=float(wsset[wsset[:,0]==obj][0][1])
		mag=lc1['Y']
		mu=float(disf[disf[:,0]==obj][0][1])
		u=m2f().slp(ph, mag)
		m5=u[0]*(t2+25)+u[1]
		print u
		if u[0]<0.1:
			ar.append(m5-mu)
			ar1.append(float(tmax[tmax[:,0]==obj][0][3]))
	except:
		obj
ar=array(ar)
ar1=array(ar1)
#print pearsonr(ar, ar1), len(ar)

#
#plot(lc1['MJD'], lc1['B'], 'r.')
#show()
wvarr=array([4330, 5456, 6156, 7472])
zparr=array([6.32, 3.63, 2.17, 1.13 ])
bands=array(['B'])#, 'V', 'r', 'i'])
bfl=[]
dmarr=[]
#for k in wsset:
#	if k in disf[:,0]:	
	#	snar=array([m2f().mag2f(k, i) for i in bands])
	#	bfl.append(m2f().trap(snar, wvarr)[0])
		#dmarr.append(float(decl[decl[:,0]==k][0][3]))		
	
bfl=[m2f().mag2f(i, 'B') for  i in wsset]
#r=[float(decl[decl[:,0]==k][0][3]) for i in wsset]
bfl=array(bfl)
print pearsonr(bfl[:,0], bfl[:,1]) #dmarr, #pearsonr(bfl, dmarr)
#tr=trapz(snar, wvarr)
 #pearsonr(arr[:,0], arr[:,1])#, 5.006743e-44*lb+3.4823e-87
#print m2f().spl_fit(obj, filt), conv().f_ord(obj)
'''