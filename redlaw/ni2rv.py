"""
Short script to calculate the Rv from the Ni mass (derived from t2), without presuming a reddening law

Needs: E(B-V), observed (uncorrected) M_B and Ni mass (or t2)

"""
import numpy as np
import matplotlib.pyplot as plt
import sys

from scipy.stats import pearsonr
rn=np.random.normal
def ni2mb(a, b):
	ar=[(-(np.log10(rn(a, b))-np.log10(2))/0.4) - 19.841 for k in range(10000)]
	return np.mean(ar), np.std(ar)

def rv_est (ni, eni, sn, qtt):
	"""
	estimate the av and rv from bolometric luminosity
	"""

	ebv=np.loadtxt('../ebvhost_csp.txt', dtype='string')
	dist=np.loadtxt('../csp_dist.txt', dtype='string')
	bmfile=np.loadtxt('../bmax_obs.txt', dtype='string')
	

	#ni=float(sys.argv[1])
	#eni=float(sys.argv[2])
	mb, emb=ni2mb(ni, eni)
	print "Estimated M_B from Nimass (t2) is:",  mb, emb	

	#sn=sys.argv[3]
	obsmb=float(bmfile[bmfile[:,0]==sn][0][1])
	
	val_ebv=float(ebv[ebv[:,0]==sn][0][1])
	val_dist=float(dist[dist[:,0]==sn][0][1])
	
	Mb=obsmb-val_dist
	
	ab=Mb-mb
	
	av=ab-val_ebv
	e_av=emb+ 0.1
	print "A_v and error are:", av, e_av
	aa=[rn(av, e_av)/rn(val_ebv, 0.01) for k in range(10000)]
	print "Mean $R_V$ and standard deviation is:",np.mean(aa), np.std(aa)

	print "E(B-V) is:", val_ebv
	if qtt=='av':		
		return av, e_av
	elif qtt=='rv':
		return np.mean(aa), np.std(aa), val_ebv
		
def main():
	lumls=np.loadtxt('../out_files/lbolhist_j.txt', dtype='string')
	nm=[]
	arr=[]
	for i in lumls:
		try:
			rv , erv, ebv=rv_est(float(i[1]), float(i[2]), 'SN'+i[0], 'rv')
			arr.append([rv, erv, ebv])
			nm.append(i[0])
		except:
			i
	
	arr=np.array(arr); nm=np.array(nm)
	#print arr,nm
	#arr=arr[arr[:,1] < 1.]
	arr=arr[arr[:,0] < 7]
	print pearsonr(arr[:,0], arr[:,-1])
	print arr, nm[arr[:,0] < 7.]
	np.savetxt('calc_rv.dat', arr)
	plt.hist(arr[:,0].astype('float32'), histtype='step')
	#plt.ylim(0, 5)
	#plt.xlim(1.5, 3.0)
	plt.xlabel('$R_V$')
	plt.ylabel('$N$')
	plt.show()
main()
