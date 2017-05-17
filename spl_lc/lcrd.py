from mag2fl import conv
from glob import glob
import numpy as np

h='/home/sdhawan/pap_files/CSP_Photometry_DR2/'
tmax=np.loadtxt('/home/sdhawan/tests_paper/ni/files_snpy/tmax_dm15.dat', dtype='string')
for i in tmax:
	try:
		lc1=conv().rd_lc(i[0], 'J')
		lc1['MJD']-=float(i[1])
		arr=np.zeros([len(lc1['MJD']), 3])
		arr[:,0]=lc1['MJD']
		arr[:,1]=lc1['J']
		arr[:,2]=lc1['e_J']
		np.savetxt('idl_lc/'+i[0]+'_lc.txt', arr)
		print i[0]
	except:
		i[0]
