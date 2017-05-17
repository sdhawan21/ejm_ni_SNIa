import numpy as np
import matplotlib.pyplot as plt
rn=np.random.normal
c=[0.04, 0.005, 0.055, 0.125]
plt.rcParams['axes.linewidth']=2.5
plt.rcParams['xtick.major.size']=12
plt.rcParams['ytick.major.size']=12
def niest(val):
	arr=np.array([rn(c[0], c[1])*rn(val[0], val[1])-rn(c[2], c[3]) for k in range(1000)])
	return np.mean(arr), np.std(arr)
yy=np.loadtxt("mod_tabY-exp.tex", delimiter="&", dtype='string')
jj=np.loadtxt("mod_tabJ-exp.tex", delimiter="&", dtype='string')
tt=[]
jt=[]
nm=[]
#np.array([[i[5][2:7], i[5][12:16]] for i in yy ])
def 
	for i in yy:
		if i[0] in jj[:,0]:
			try:
				jk=jj[jj[:,0]==i[0]][0][5]
				jt.append([float(jk[2:7]), float(jk[12:16])])
				tt.append([float(i[5][2:7]), float(i[5][12:16])])
				nm.append(i[0])
			except:
				i[0]
	tt=np.array(tt)
	jt=np.array(jt)
	narr=np.array([niest(i) for i in tt ])
	narr[:,0]/=2
	jnarr=np.array([niest(i) for i in jt])
	jnarr[:,0]=jnarr[:,0]/2
	dif=jnarr[:,0]-narr[:,0]
	vs=np.vstack([nm, jnarr[:,0], jnarr[:,1], narr[:,0], narr[:,1]]).T
#np.savetxt("../../arn_dev/yjtab.dat", vs, fmt='%s')
def pltarr():
	s=plt.subplot(111)
	s.minorticks_on()
	s.tick_params('both', length=15, width=2, which='major')
	s.tick_params('both', length=7, width=2, which='minor')
	plt.xlim(0.2, 0.8)
	plt.ylabel('$M_{Ni}$(J)-$M_{Ni}$(Y)')
	plt.xlabel('$M_{Ni}$(J)')
	plt.errorbar(jnarr[:,0], dif, jnarr[:,1], fmt='ro')
#plt.show()
print np.mean(abs(dif))
