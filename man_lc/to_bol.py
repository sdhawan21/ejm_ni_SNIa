import numpy as np

r=np.loadtxt('raw/11fe_raw.dat',usecols=(0, 1, 3,4, 6, 7, 9, 10, 12))
fil=['B', 'V', 'R', 'I']
#ff=open("11fe_bol.dat", 'w')
nfil=4
fir=['J', 'H']
c=[1, 3, 5, 7]
p=0
pt='/home/sdhawan/Downloads/CSP_Photometry_DR2/lc_band_sn/'
for k in range(nfil):
	#ff.write('#FILTER\t'+fil[k]+'_BESSELL\t'+str(len(r))+'\tMEASUREMENTS\n')
	#for i in r:
	bnd=r[:,[0, c[k], c[k]+1]]
	np.savetxt(pt+'11fe_'+fil[k]+'.dat', bnd)
		#ff.write(i[0]+' '+i[c[k]]+' '+i[c[k]+1]+'\n')
		#p=k+1
#ff.close()
ir_fil=['J', 'H']	
r1=np.loadtxt('raw/ir_11fe_raw.dat', usecols=(0, 1, 2, 3, 4, 5, 6), dtype='string')
#arr=np.zeros()
#arr[:,0]=r1[:,0].astype('float32')
fout=open('ir_11fe.dat', 'w')
xprec=5
yprec=5
zprec=5
for k in range(2):
	ind=1+2*k
	eind=2+2*k
	u=r1[:,ind].astype('float32')
	r2=r1[u<90]
	sc=len(r1[u<90])
	arr=np.zeros([sc, 3])
	arr[:,0]=r2[:,0].astype('float32')-55000
	r2[:,ind].astype('float32')
	#o=[float(i)-55000 for i in r2[:,ind]]
	#r2[:,ind]-=55000
	arr[:,1]=r2[:,ind].astype('float32')
	y=[float(i[eind][1:-1])/100.0 for i in r2 ]
	#fout.write('#FILTER\t'+fir[k]+'_CSP-\t'+str(len(u[u<90]))+'\tMEASUREMENTS (MJD MAG MAGERR)\n')
	#y=np.array([i[eind][1:-1]/100.0 for i in r1])
	arr[:,2]=y
	np.savetxt(pt+'11fe_'+fir[k]+'.dat', arr)
	#for l in r1:
	#	a=float(l[0])
	#	b=float(l[ind])
	#	c=float(l[eind][1:-1])/100.0
	#	if b<90:
	#		print >> fout, "%.*g  %.*g  %.*g" % (xprec, a, yprec, b, zprec, c)
	#arr[:,(1+2k)]=r1[:,(1+2k)].astype('float32')
	#y=np.array([float(i[1:-1])) for i in r1[:,(2+2k)]])
	#arr[:,(2+2k)]=y



