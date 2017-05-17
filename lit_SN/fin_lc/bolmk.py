import numpy as np
import sys


pt='/home/sdhawan/Downloads/CSP_Photometry_DR2/lc_band_sn/'
filt=['B', 'V', 'R',  'I']
irf=['J', 'H']
nm=sys.argv[1]
if sys.argv[2]=='a':
	cols=[0,  3, 4, 5, 6, 7, 8, 9, 10]
elif sys.argv[2]=='b':
	cols=[0, 1, 2, 3, 4, 5, 6]
else:
	cols=[1, 4, 5, 6, 7]
opt=np.loadtxt(nm+'_opt.ascii', usecols=(cols), dtype='string', delimiter='&')#, dtype='string')
#print opt[:,0]
ir=np.loadtxt(nm+'_ir.ascii', usecols=(1,3 , 5,6, 8)) #dtype='string')#, delimiter='&')#, dtype='string')


for j in range(len(filt)):
	p=opt[:,0]
	ind=1+j
	#eind=ind+1
	#con=opt[:,ind]!='\nodata'
	p=[]; m=[];me=[]
	for i in opt:
		try:
			m.append(float(i[ind][1:6]))#
			me.append(float(i[ind][12:17])) # for i in opt[:,ind][con]]
			p.append(float(i[0]))
		except: 
			i
	#me=opt[:,eind]
	#me=[float(i[8:12]) for i in opt[:,ind][con]]
	sc=len(m)
	arr=np.zeros([sc, 3])
	p=np.array(p); m=np.array(m); me=np.array(me)
	#print m<90
	con=m<90
	print p, m, me
	arr[:,0]=p#[con]
	arr[:,1]=m#[con]
	arr[:,2]=me#[con]
	np.savetxt(pt+nm+'_'+filt[j]+'.dat', arr)
for lm in range(len(irf)):
	p=ir[:,0]
	ind=1+2*lm
	eind=ind+1
	m=ir[:,ind]
	me=ir[:,eind]
	con=m<90
	sc=len(m[con])
	arr=np.zeros([sc, 3])
	arr[:,0]=p[con]
	arr[:,1]=m[con]
	arr[:,2]=me[con]
	np.savetxt(pt+nm+'_'+irf[lm]+'.dat', arr)
'''
for j in range(len(filt)):
	p=opt[:,0]
	ind=1+2*j
	eind=ind+1
	m=opt[:,ind]
	me=opt[:,eind]
	con=m<90
	sc=len(m[con])
	arr=np.zeros([sc, 3])
	arr[:,0]=p[con]
	arr[:,1]=m[con]
	arr[:,2]=me[con]
	np.savetxt(pt+nm+'_'+filt[j]+'.dat', arr)


for lm in range(len(irf)):
	p=ir[:,0]
	ind=1+lm
	#eind=ind+1
	p=[]; m=[];me=[]
	for i in ir:
		try:
			m.append(float(i[ind][1:7]))#
			me.append(float(i[ind][9:13])) # for i in opt[:,ind][con]]
			p.append(float(i[0]))
		except: 
			i
	print m, p, me
	sc=len(m)
	arr=np.zeros([sc, 3])
	p=np.array(p); m=np.array(m); me=np.array(me)
	arr[:,0]=p
	arr[:,1]=m
	arr[:,2]=me
	np.savetxt(pt+nm+'_'+irf[lm]+'.dat', arr)
'''