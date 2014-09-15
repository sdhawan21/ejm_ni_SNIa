import numpy as np
import sys
import matplotlib.pyplot as plt


from glob import glob
from bol_lc import bol_lc
from scipy.interpolate import interp1d
from scipy.stats import pearsonr
sys.path.append('../tests_paper/ni/files_snpy/')
sys.path.append('../tests_paper/csp_sn/sec_max_files/')
pt=sys.path
#obj=sys.argv[1]
class rise:
	def tmax(self, sn, bands):
		lc1=bol_lc().rd_bol(sn, bands)
		sp=interp1d(lc1[:,0], lc1[:,1], kind='cubic')
		l=np.linspace(min(lc1[:,0]), max(lc1[:,0]), 100)
		gp=sp(l)
		tm=l[gp==max(gp)]
		return tm, max(gp)
	def rise_t(self, sn, bands):
		lc1=bol_lc().rd_bol(sn, bands)
		m=self.tmax(sn, bands)
		ph=lc1[:,0]-m[0]
		ph1=ph[ph<=0]
		mag1=2.5*np.log10(lc1[:,1][ph<=0])
		l1=np.linspace(min(ph1), max(ph1), 100)
		spl=interp1d(ph1, mag1, kind='cubic')
		msp=spl(l1)
		m7=msp-(2.5*np.log10(m[1])-1)
		return l1[abs(m7)==min(abs(m7))]
		
n=np.loadtxt('rise_inf.txt', dtype='string')
sn=n[:,0]
#sset=sorted(glob('lcbol_distrib/*lcbol*'))
r=[]
dec=[]
dm=np.loadtxt(pt[-2]+'tmax_dm15.dat', dtype='string')
for i in sn:
	try:
		ph=bol_lc().rd_bol('sn'+i[2:len(i)], 'BVRIJH')[:,0]-rise().tmax('sn'+i[2:len(i)], 'BVRIJH')[0]
		r.append([rise().rise_t('sn'+i[2:len(i)], 'BVRIJH')[0], min(ph)])
		dec.append([float(n[n[:,0]==i][0][1]), float(dm[dm[:,0]==i][0][3])])
		print i
	except:
		i
r=np.array(r)
dec=np.array(dec)
#plt.hist(r[:,0], histtype='step')
plt.hist(dec[:,0], alpha=0.2, label='b_band')
plt.hist(r[:,0], alpha=0.2, label='bolometric')
plt.legend(loc=2)
plt.show()
print pearsonr(r[:,0], dec[:,0]), r[:,0]-dec[:,0]		
#print rise().rise_t(obj, 'BVRIJH'), min(bol_lc().rd_bol(obj, 'BVRIJH')[:,0]-rise().tmax(obj, 'BVRIJH')[0])
# rise().rise_t('sn2006ax', 'BVRIJH'), min(bol_lc().rd_bol('sn2006ax', 'BVRIJH')[:,0]-rise().tmax('sn2008hv', 'BVRIJH')[0]),  rise().tmax('sn2008hv', 'BVRIJH')[0]
