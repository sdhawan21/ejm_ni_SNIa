from numpy import loadtxt, polyfit, linspace
from glob import glob
from sys import argv
#fout=open('lit_t1m1'+argv[1]+'.txt', 'w')
from matplotlib.pyplot import *
sam=sorted(glob('fin_lc/'+argv[1]+'_band/*'))
par=loadtxt('params.txt', dtype='string')
sn2=[i[0][4:len(i[0])] for i in par ]
nd=int(argv[2])
lim=int(argv[3])
for j in range(1):
	i=sam[j+nd]
	lc=loadtxt(i)
	lc1=lc[lc[:,1]<99]
	nm=i[14:len(i)-8]
	if nm in sn2:	
		t=float(par[list(sn2).index(nm)][1])
		lc1[:,0]=lc1[:,0]-t
		lc2=lc1[lc1[:,0]<lim]
		pf=polyfit(lc2[:,0], lc2[:,1], 3)
		l=linspace(-15, max(lc2[:,0]), 100)
		fi=pf[0]*l**3+pf[1]*l**2+pf[2]*l+pf[3]
		m1=min(fi)
		errorbar(lc2[:,0], lc2[:,1], fmt='b.')
		plot(l, fi)
		t1=l[list(fi).index(min(fi))]
		print m1, t1
		#fout.write(nm+'\t'+str(m1)+'\t'+str(t1)+'\n')
show()
#fout.close()
