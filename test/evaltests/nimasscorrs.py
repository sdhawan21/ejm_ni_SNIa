import numpy as np
import matplotlib.pyplot as plt

from pack import bol
from scipy.stats import pearsonr, ks_2samp
from scipy.odr import *

infile=np.loadtxt('../../s14_files/snmcmc_results_runBp_mlo.txt', dtype='string')


dmfile=np.loadtxt('/home/sdhawan/tests_paper/ni/files_snpy/tmax_dm15.dat', dtype='string')

t2file=np.loadtxt('/home/sdhawan/tests_paper/csp_sn/sec_max_files/y_sec_max_csp.dat', dtype='string')


def readni():
	
	
	
	
	
	
	
	dmarr=np.array([float(dmfile[dmfile[:,0]==i[0]][0][3]) for i in infile if i[0] in dmfile[:,0]])
	print dmarr
	niarr=np.array([float(i[19]) for i in infile if i[0] in dmfile[:,0]])
	
	nidm15=-0.61*dmarr+1.30
	
	dif=nidm15-niarr
	return dif, niarr


def evalslp(a, b, c, d):
	"""
	Compact use of scipy.odr
	"""
	
	def f(B, x):
		return B[0]*x+B[1]
	rd=RealData(a, c, sx=b, sy=d)
	f=Model(f)
	out=ODR(rd, f, beta0=[1., 2.])
	od=out.run()
	return od.beta, od.sd_beta
	
	
def calib_snmcmc():
	"""
	Use the Ni masses from Richard to calibrate the relation with which the t2 is used to calculate Mni
	
	Uses scipy.odr
	
	"""
	
	t2arr=[float(t2file[t2file[:,0]==i[0]][0][1]) for i in infile if i[0] in t2file[:,0]]
	
	et2arr=[float(t2file[t2file[:,0]==i[0]][0][2]) for i in infile if i[0] in t2file[:,0]]
	
	niarr=np.array([float(i[19]) for i in infile if i[0] in t2file[:,0]])
	eniarr=np.array([float(i[20]) for i in infile if i[0] in t2file[:,0]])
	
	
	
	mc, emc = evalslp(t2arr, et2arr, niarr, eniarr)
	
	t2excl=np.array([float(i[1]) for i in t2file if i[0] not in infile[:,0] and i[0] in dmfile[:,0]])
	
	dmexcl=np.array([float(dmfile[dmfile[:,0]==i[0]][0][3])  for i in t2file if i[0] not in infile[:,0] and i[0] in dmfile[:,0]])
	
	t=mc[0]*t2excl+mc[1]
	print pearsonr(niarr, t2arr)
	plt.plot(niarr, t2arr, 'r+')
	plt.show()
	dm=-0.61*dmexcl+1.3
	return t, (0.04*t2excl-0.047)/2, t2excl#niarr, (0.043*np.array(t2arr)-0.1)/2#t, dm


def d15t2():
	"""
	Compare t2 estimates to the estimates from 
	"""
	darr=np.array([-0.61*float(i[3])+1.3 for i in dmfile if i[0] in t2file[:,0]])
	
	uarr=np.array([(0.04*float(t2file[t2file[:,0]==i[0]][0][1])-0.1)/2.0 for i in dmfile if i[0] in t2file[:,0]])
	
	
	return uarr, darr
	

def main():
	peak=np.loadtxt('/home/sdhawan/bol_ni_ej/peaknicomp.txt', dtype='string', skiprows=1)
	
	dmarr=np.array([float(dmfile[dmfile[:,0]==i[0]][0][3]) for i in peak if i[0] in dmfile[:,0]])
	
	ni=np.array([float(i[1]) for i in peak if i[0] in dmfile[:,0]])
	ni1=-0.61*dmarr+1.3
	
	nit2=np.array([float(i[2]) for i in peak if i[0] in dmfile[:,0]])
	
	t2rs, t2, t2excl=calib_snmcmc()
	print t2rs, t2excl
	#print pearsonr(ni, ni-nit2), max(ni-nit2)
	return 0
	plt.hist(ni1, histtype='step')
	plt.hist(ni, histtype='step')
	plt.show()
	
	
	
	
	
	
	

main()
