#from eni_alph_arn import alp_cons as ac

import matplotlib.pyplot as plt
import numpy as np
import sys
rn=np.random.normal
dm=np.loadtxt('/home/sdhawan/bol_ni_ej/tmax_dm15.dat', dtype='string')
def eqarn(tr):
	return 6.45*np.exp(-tr/8.8)+1.45*np.exp(-tr/111.3)  
def ufl():
	gg=np.loadtxt('/home/sdhawan/bol_ni_ej/tables/u_flags.txt', dtype='string')
	dm1=[[float(i[1])/2, float(dm[dm[:,0]==i[0]][0][3])] for i in gg if i[0] in dm[:,0]]
	dm1=np.array(dm1); tr=17.5-5*(dm1[:,1]-1.1)
	return dm1[:,0], tr
	
ddc_mod=np.loadtxt('lpeak_m56ni.dat', usecols=(1,   3, 4, 7, 8, 2))
def rise_plt():
	ind=int(sys.argv[1])
	arr=[]
	for ind in range(len(ddc_mod)):
		lm_ni=ddc_mod[ind][4]/ddc_mod[ind][0]
		pr_tr=np.linspace(15, 22, 100)
		ll=np.array([eqarn(i) for i in pr_tr])-lm_ni
		trp=pr_tr[abs(ll)==min(abs(ll))]
		print trp
		arr.append([ddc_mod[ind][0], trp ,lm_ni])
	arr=np.array(arr)
	#np.savetxt("rise_models_comp.txt", np.array(arr))
	b=ufl()
	b=np.sort(b, axis=0)
	plt.plot(b[0], b[1], 'r.')
	plt.scatter(arr[:,0], arr[:,1])
	plt.xlabel('$M_{Ni}$')
	plt.ylabel('$Rise (days)$')
#plt.scatter(ddc_mod[:,3], ddc_mod[:,-1]/ddc_mod[:,3])
print 0.58/eqarn(14), 0.58/eqarn(16) 
#rise_plt()
#plt.show()























'''
def sdnorm(z):
	"""
	standard normal pdf
	"""
	return np.exp(-(z-16.5)**2/2*(4))/np.sqrt(2*np.pi*2)	
n=1000
alpha=1
innov=np.random.uniform(-alpha, alpha, n)
def mhalg(innov, n):
	x=0
	vec=[]
	for i in range(n):
		can=x+innov[i]
		try:
			aprob=min([1, sdnorm(can)/sdnorm(x)])
			u=np.random.uniform(0, 1, 1)
			if u < aprob:
				x = can
				vec.append(x)	
		except:
			x
	return vec
tr=np.array([rn(19, 3) for k in range(1000)])
def earn(tr, alpha):
	eni=6.45e43*np.exp(-tr/8.8)+1.45e43*np.exp(-tr/111.3)
	return eni*alpha
earr=earn(tr, alpha)
print np.mean(earr), np.std(earr)
plt.scatter(tr, earr)
plt.show()
'''
