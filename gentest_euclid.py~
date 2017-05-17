import numpy as np
import sys
import os

#from astropy.cosmology import wCDM, w0waCDM

homept = os.path.expanduser('~')
euc_path = homept+'/workspaces/euclid_mcgen/'
zpath = euc_path + 'zdist/mcmc_files/z_euclid_perrett_highz.dat'
dirjw_file = homept+'/workspaces/multinest_cosmology/emcee/sim_txt/perrett_cut77_jwst_300err.dat'


def mock_hdreal(scatrm , outfile, mean=False, meanval=-19.5, nsn=1000, seed = True, seedval=2223):
	if seed:	
		np.random.seed(seedval)
	inp = np.loadtxt(dirjw_file, skiprows=2, usecols=(1,2,3))
	z = inp[:,0][inp[:,1]<0.]
	mmag = np.mean(inp[:,1][inp[:,1]<0.])
	err = inp[:,2][inp[:,1]<0.]
	if mean:
		mmag = meanval
		z = np.random.uniform(0.05, 1.5, nsn)
		err = np.random.uniform(0.04, 0.09, nsn)	
	reals = np.random.normal(mmag, scatrm, len(z))
	sn1 = np.array(['sn'+str(i) for i in range(len(err))])
	vs = np.vstack([sn1, z, reals, err]).T
	np.savetxt(outfile, vs, fmt='%s')
