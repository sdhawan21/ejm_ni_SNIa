import numpy as np
import matplotlib.pyplot as plt
import sys

from scipy.interpolate import interp1d


rn=np.random.normal
def interp_mb():
	s1=np.loadtxt('../ni_logbol_c00.txt', usecols=(1, 3))
	s1[:,1]=pow(10, s1[:,1])
	s1[:,1]/=1e43
	s1[:,0]=abs(s1[:,0])
	s1=s1[s1[:,1].argsort()]  
	lbol=s1[:,1]
	lbol=np.delete(lbol, 2)
	mb=np.delete(s1[:,0], 2)
	gl=interp1d(lbol,mb , kind='cubic')
	l=np.linspace(lbol.min(), lbol.max())
	spl=gl(l)
	tl=float(sys.argv[1])
	etl=float(sys.argv[2])
	ex_arr=[]
	pf=np.polyfit(lbol, mb, 2)
	bf=pf[0]*tl**2+pf[1]*tl+pf[2]
	#print bf
	#plt.plot(lbol, mb, 'r+')
	#plt.show()
	for k in range(1000):
		l1=abs(l-rn(tl, etl))
		ex=spl[l1==min(l1)]
		ex_arr.append(ex[0])
	return np.mean(ex_arr), np.std(ex_arr)
if len(sys.argv)==3:	
	print interp_mb()[0]+14.111-30.91, interp_mb()[1]+0.14+0.011
else:
	print "Usage: python "+sys.argv[0]+"<Lbol peak > <e_Lbol>"
