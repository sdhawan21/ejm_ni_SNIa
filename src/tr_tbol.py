import numpy as np
import matplotlib.pyplot as plt
#import mag2fl as mf

from matplotlib.font_manager import FontProperties
from glob import glob
from scipy.interpolate import interp1d

fp=FontProperties(family='times new roman', size=30)

class fil_manip:
	darr=np.loadtxt('../tmax_dm15.dat', dtype='string')
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
	def pl(self, arr):
		plt.figure(figsize=(12, 18))
		
		plt.rcParams['axes.linewidth']=2.5
		plt.rcParams['xtick.major.pad']=6
		plt.rcParams['ytick.major.pad']=4
		plt.ylim(0.0, 4.0)
		sp=plt.subplot(111)
		sp.minorticks_on()
		sp.tick_params('both', length=15, width=2)
           	sp.tick_params('both', length=7, width=2, which='minor')
           	frame=plt.gca()
           	ytickar=frame.axes.get_yticklabels()
	   	
	   	for ylab in ytickar:
	 
	   		ylab.set_fontproperties(fp) 
	   		
	   	ytickar[0].set_visible(False) 
	   	ytickar[-1].set_visible(False)
		plt.hist(arr, alpha=0.3, bins=np.arange(-3, 1, 0.5), color='r')
		for xlab in frame.axes.get_xticklabels():
	   			xlab.set_fontproperties(fp) 
		plt.xlabel('$t_{R,bol}$-$t_{R, B}$', fontsize=30, labelpad=6)
		plt.ylabel('$N_{SN}$', fontsize=30, labelpad=30)
		return plt.savefig('../plot_rel/tbol_tb.pdf')

def main():
	sset=sorted(glob('../lcbol_distrib/finfiles/utest/*.dat'))
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
	#plt.hist(tbol, color='r', alpha=0.3)
	print np.mean(tbol), len(tbol), len(sset)
	#plt.show()
	fil_manip().pl(tbol)
main()
