import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import MultipleLocator
from matplotlib import font_manager

pt='/home/sdhawan/tests_paper/csp_sn/sec_max_files/'
pt1='/home/sdhawan/bol_ni_ej/'
def arr(bd):
	uir=np.loadtxt(pt1+'tables/u_flags.txt', dtype='string', skiprows=1)
	uir=uir[uir[:,3]=='UBVRIJH']
	t2=np.loadtxt(pt+bd+'_sec_max_csp.dat', dtype='string')
	t=[float(i[1]) for i in t2 if i[0] in uir[:,0]]
	ni=[float(uir[uir[:,0]==i[0]][0][1]) for i in t2 if i[0] in uir[:,0]]
	ne=[float(uir[uir[:,0]==i[0]][0][2]) for i in t2 if i[0] in uir[:,0]]
	et=[float(i[2]) for i in t2 if i[0] in uir[:,0]]
	return t, ni, ne, et
def main():
	plt.rcParams['axes.linewidth']=2.5
	#plt.rcParams['xaxis.major.size']=12
	#plt.rcParams['yaxis.major.size']=12
	fig=plt.figure(figsize=(12, 18))
	fil=['y', 'j', 'h']
	s=[311,312,310]
	f=['yD', 'g.', 'rs']
	corr=[[0.04, -0.055],[0.042, -0.039],[0.033, -0.239]]
	for i in range(3):
           sp=plt.subplot(s[i])
           sp.minorticks_on()
           sp.tick_params('both', length=15, width=2)
           sp.tick_params('both', length=7, width=2, which='minor')
	   plt.xlim(10, 40)
	   t,n,ne,et=arr(fil[i])
	   plt.errorbar(t, n, xerr=et, yerr=ne, fmt=f[i], ms=10)
	   t=np.array(t);#bf=corr[i][0]*t+corr[i][1]
	   vs=np.vstack([t, np.ones(len(t))]).T; a=np.linalg.lstsq(vs, n)[0]; print a, len(t)
	   plt.plot(t, a[0]*t+a[1], 'k:')
	#frame=gca()
	#if s[i]!=310:
		#frame.xticklabels()
	plt.subplots_adjust(hspace=0)
	plt.xlabel('$t_2(days)$')
	plt.subplot(312)
	plt.ylabel('$L_{Bol}$')
	plt.savefig('lbolt2_bf.pdf')

main()
