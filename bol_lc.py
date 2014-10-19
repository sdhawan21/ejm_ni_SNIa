"""analysis of the bolometric light curves fit using stephane's routine in IDL (mklcbol.pro)"""
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../tests_paper/ni/files_snpy/')
sys.path.append('../tests_paper/csp_sn/sec_max_files/')
pt=sys.path
from scipy.odr import *
from scipy.interpolate import interp1d
from scipy.stats import pearsonr
class bol_lc:
	def f(self, B, x):
		return B[0]*x+B[1]
	def rd_bol(self,sn, bands):
		return np.loadtxt('lcbol_distrib/'+sn+'_lcbol_'+bands+'.dat')
	def lt_dec(self, sn, bands):
		lc1=self.rd_bol(sn, bands)
		sp=interp1d(lc1[:,0], lc1[:,1], kind='cubic')
		l=np.linspace(min(lc1[:,0]), max(lc1[:,0]), 100)
		gp=sp(l)
		tm=l[gp==max(gp)]
		ph=lc1[:,0]-tm
		ph1=ph[(ph>=40) & (ph<=90)]
		mag=np.log10(lc1[:,1][(ph>=40) & (ph<=90) ])
		a=np.vstack([ph1, np.ones(len(ph1))]).T
		y=np.linalg.lstsq(a, mag)[0]
		return y
	def odr_dec(self, sn, bands):
		lc1=self.rd_bol(sn, bands)
		sp=interp1d(lc1[:,0], lc1[:,1], kind='cubic')
		l=np.linspace(min(lc1[:,0]), max(lc1[:,0]), 100)
		gp=sp(l)
		tm=l[gp==max(gp)]
		ph=lc1[:,0]-tm
		ph1=ph[(ph>=40) ]
		mag=np.log10(lc1[:,1][(ph>=40) ])
		mage=np.log10(lc1[:,2][(ph>=40) ])
		rd=RealData(ph1, mag, sy=mage)
		f=Model(self.f)
		out=ODR(rd, f, beta0=[1., 2.])
		o=out.run()
		return o.beta, o.sd_beta
	def dm15_bol(self, sn, bands):
		lc1=self.rd_bol(sn, bands)
		sp=interp1d(lc1[:,0], lc1[:,1], kind='cubic')
		l=np.linspace(min(lc1[:,0]), max(lc1[:,0]), 100)
		gp=np.log10(sp(l))
		tm=l[gp==max(gp)]
		ph=lc1[:,0]-tm
		if min(ph)<0:
			ph1=abs(l-15)
			m15=gp[ph1==min(ph1)][0]
			return max(gp)-m15#np.log10(max(gp))-np.log10(m15)	
		else:
			return 99.0
class t2_ni:
	def fils(self):
		ni=np.loadtxt('mni_lcbol.txt', skiprows=1, dtype='string')
		t2=np.loadtxt(pt[-1]+'j_sec_max_csp.dat', skiprows=1, dtype='string')
		return ni, t2
	def lin_fit(self):							# linear fit to the Nickel mass-t2 arrays
		ni, t2=self.fils()						# only illustrative, no physical reason why, use interp insteda
		n=[float(ni[ni[:,0]==i[0]][0][1]) for i in t2 if i[0] in ni[:,0]]
		t=[float(i[1]) for i in t2 if i[0] in ni[:,0]]
		et=[float(i[2]) for i in t2 if i[0] in ni[:,0]]
		en=[float(ni[ni[:,0]==i[0]][0][2]) for i in t2 if i[0] in ni[:,0]]
		A=np.vstack([t, np.ones(len(t))]).T
		return  n, t, en, et
	def interp_fit(self, t2):
		n, t=self.lin_fit()
		sp1=interp1d(t,n, kind='cubic' )
		l1=np.linspace(min(t), max(t), 100)
		g1=sp1(l1)
		lnew=abs(l1-t2)
		return g1[lnew==min(lnew)]
class lpeak_ni:
	def int_peak(self, lp):
		r=np.loadtxt('lpeak_m56ni.dat', skiprows=5, usecols=(4, 1))
		arr_lp=np.linspace(min(r[:,0]), max(r[:,0]), 100)
		fn=interp1d(r[:,0], r[:,1], kind='cubic')                                                                                                                           
		new_arr=abs(arr_lp-lp)
		garr=fn(arr_lp)
		return garr[new_arr==min(new_arr)]
	def p2ni(self, sn, bands):
		t=bol_lc().rd_bol(sn, bands)
		r1=np.random.normal(t[:,1], t[:,2])
		p=interp1d(t[:,0], r1, kind='cubic')
		o=np.linspace(min(t[:,0]), max(t[:,0]), 100)
		u=p(o)
		return max(u)/2e43#self.int_peak(max(u)/1e43)
	def p2sing(self, sn, bands):
		t=bol_lc().rd_bol(sn, bands)
		#r1=np.random.normal(t[:,1], t[:,2])
		p=interp1d(t[:,0], t[:,1], kind='cubic')
		o=np.linspace(min(t[:,0]), max(t[:,0]), 100)
		u=p(o)
		return max(u)/1e43
	def app2ni(self, sn, bands, dm):
		n=self.p2ni(sn, bands)
		ds=3.08*1e24*pow(10, (dm-25)/5.0)
		return n*4*np.pi*(ds**2)
	def c00_p2ni(self, sn, bands):
		cni=np.loadtxt('ni_logbol_c00.txt', usecols=(3, 5))
		cni[:,0]=pow(10, cni[:,0])/1e43
		a=np.vstack([cni[:,0], np.ones(len(cni))]).T
		m=np.linalg.lstsq(a, cni[:,1])[0]
		return m[0]*self.p2ni(sn, bands)*2+m[1]
	def ni_sn(self, sn, bands):
		arr=np.array([self.c00_p2ni(sn, bands) for k in range(1000)])
		return np.mean(arr[arr<1.5]), np.std(arr[arr<1.5])
		
mni=np.loadtxt('mni_lcbol.txt', skiprows=1, dtype='string')
nm=[]
dec=[]
dm=np.loadtxt(pt[-2]+'tmax_dm15.dat', dtype='string')
lp=np.loadtxt('lpeak_m56ni.dat', usecols=(1, 4))
l1=np.linspace(min(lp[:,1]), max(lp[:,1]), 100)
spl=interp1d(lp[:,1], lp[:,0], kind='cubic')
gpl=spl(l1)
t2=np.loadtxt(pt[-1]+'j_sec_max_csp.dat', dtype='string')
#(float(t2[t2[:,0]==i][0][1])+20)

for j in mni:
	i=j[0]
	#print i
	try:
	   #l=lpeak_ni().int_peak(lpeak_ni().p2ni('sn'+i[2:len(i)], 'BVRIJH')*2)
	   dec.append([l, i])
	   #nm.append(bol_lc().lt_dec('sn'+i[2:len(i)], 'BVRIJH')[0]*55+bol_lc().lt_dec('sn'+i[2:len(i)], 'BVRIJH')[1])
	   #dec.append(bol_lc().dm15_bol('sn'+i[2:len(i)], 'BVRIJH'))#float(dm[dm[:,0]==i][0][3]))
	except:
		i
dec=np.array(dec)		
nm=np.array(nm)
fout=open('ni_dm15.txt', "a")
'''
for i in mni[:,0]:
	try:
		sn='sn'+i[2:len(i)]
		arr=np.array([lpeak_ni().p2ni(sn, 'BVRI') for i in range(1000)])
		m=np.mean(arr)
		sig=np.std(arr)
		print m, sig
		fout.write(sn+'\t'+str(m)+'\t'+str(s)+'\n')
		
	except:
		print sn
'''
#arr=[lpeak_ni().p2ni(sys.argv[1], sys.argv[2]) for i in range(1000)]
#print np.mean(arr), np.std(arr)

 #bol_lc().lt_dec(sys.argv[1], sys.argv[2]), bol_lc().odr_dec(sys.argv[1], sys.argv[2])#np.mean([lpeak_ni().p2ni(sys.argv[1], sys.argv[2]) for i in range(1000)]) #pearsonr(nm[dec<99], dec[dec<99]), dec, lpeak_ni().p2ni('SN2005hc', 'BVRIJH')
'''
nm=np.array(nm)
x=round(np.std(nm[nm<-0.02]), 4)
mu=round(np.mean(nm[nm<-0.02]), 4)
plt.hist(nm[nm<-0.02], label='bol. decl.')
plt.annotate('std='+str(x)+'\n'+'mean='+str(mu), xy=(0.1, 0.8), xycoords='axes fraction')
plt.xlabel('Decline rate')
plt.ylabel('Number')
t14j=t2_ni().interp_fit
tcorr=t2_ni().lin_fit
s=tcorr()
print pearsonr(tcorr()[0], tcorr()[1])
#print lpeak_ni().p2ni('sn2006D', 'BVRIJH')#np.std([t14j(np.random.normal(28.7, 5.7)) for k in range(1000)])
plt.figure(2)
plt.errorbar(s[1], s[0], xerr=s[3], yerr=s[2], fmt='g^')
#print x, mu 
#print t2_ni().lin_fit()[0]*28.7+t2_ni().lin_fit()[1]
plt.savefig('ni_t2.pdf')
#plt.savefig('Late_decl_distrib.pdf')
'''
