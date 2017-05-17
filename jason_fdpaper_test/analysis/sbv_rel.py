import numpy as np
import matplotlib.pyplot as plt

from pack import bol
from glob import glob

#define the functions for linfit and spline
bp = bol.bol_func().bolpeak
od = bol.linfits().freq_odr


#direc = '../bolometric/'
direc = '../../lowred_samp/tot_csp/bolometric/1_7/noir/'
sn_bol = glob(direc+'*.dat')

#u-band coverage is a necessity
sn_bol_u = [i for i in sn_bol if 'u_CSP' in i and 'i_CSP' in i]

sbv_file = np.loadtxt('../../sbv_all_b14.txt', dtype='string')
ebv_file = np.loadtxt('../../ebvhost_csp.txt', dtype='string')

finarr=[]
finarr_nonames=[]
for i in sn_bol_u:
	snname = i[46:-36]
	
	if snname in sbv_file[:,0] and snname in ebv_file[:,0]:
		ebvhost = float(ebv_file[ebv_file[:,0]==snname][0][1])
		lc = np.loadtxt(i)
		if  ebvhost < .3:
			s = sbv_file[sbv_file[:,0]==snname][0]
			finarr.append([snname, s[1],s[2], bp(i)[0]/1e43, lc[lc[:,1]==max(lc[:,1])][0][2]/1e43])
			#err_arr = [bol.bol_func().err_peak(lc)[0]/1e43 for k in range(1000)]
			finarr_nonames.append([float(s[1]), float(s[2]), float(bp(i)[0]/1e43), lc[lc[:,1]==max(lc[:,1])][0][2]/1e43])
		
finarr = np.array(finarr)
finarr_nonames = np.array(finarr_nonames)


np.savetxt('sbv_lmax_all_noir.dat', finarr, fmt='%s')
print "Fast", od(finarr_nonames[finarr_nonames[:,2]<.4])
print "Normal", od(finarr_nonames[finarr_nonames[:,2]>.4])

f=finarr_nonames
plt.errorbar(f[:,0], f[:,2], xerr=f[:,1], yerr=f[:,3], fmt='gs')
plt.show()
