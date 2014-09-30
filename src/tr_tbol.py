import numpy as np
import matplotlib.pyplot as plt
#import mag2fl as mf


from glob import glob
from scipy.interpolate import interp1d
class fil_manip:
	darr=np.loadtxt('tmax_dm15.dat', dtype='string')
	def indval(self, i, num):
		return self.darr[self.darr[:,0]==i][0][num]
	def rdfil(self, fil):
		t=open(fil, 'r')
		ls=[]
		for row in t:
			ls.append(row.split())
		return ls[3][1]		
	def bpk(self, fil):
		tt=np.loadtxt(fil)
		spl=interp1d(tt[:,0], tt[:,1], kind='cubic')
		l=np.linspace(min(tt[:,0]), max(tt[:,0]), 100)
		fpl=spl(l)
		return l[fpl==max(fpl)][0]
	def pl(self):
		plt.hist(tbol, alpha=0.3)
		plt.xlabel('$t_R(bol)$-$t_R{B}$')
		plt.ylabel('$N_{SN}$')
		return plt.savefig('plot_rel/tbol_tb.pdf')
sset=sorted(glob('lcbol_distrib/finfiles/utest/*.dat'))
rf=fil_manip().rdfil	#read names
bt=fil_manip().bpk	#bolometric peak
dd=fil_manip().indval	#b-peak
#print dd(rf(sset[0]), 1), bt(sset[0])
tbol=[]
for i in sset:
	try:
		if rf(i) in fil_manip().darr[:,0]:
			x=bt(i)-float(dd(rf(i), 1))
			tbol.append(x)
	except: 
		i
		
#print tbol, np.mean(tbol)
print np.median(tbol), len(tbol), len(sset)
#fil_manip().pl()
