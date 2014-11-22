from pack import dist

import numpy as np
import sys

def main():
	mm=np.loadtxt('ddc_model.dat', dtype='string', usecols=(1, 2, 3), skiprows=1)

	farr=['Y', 'J', 'H']	
	filt=sys.argv[1]
	sub=mm[mm[:,0]==filt]
	mag_arr=sub[:,2].astype('float32')
	magnorm=mag_arr[mag_arr>-999.999]
	magnorm=magnorm[:-1]
	ind=farr.index(filt)
	zp=[-2.74, -2.72, -2.667]
	ezp=[0.01, 0.01, 0.02]
	
	m=[np.mean(magnorm), np.std(magnorm)/np.sqrt(len(magnorm))]
	#print magnorm
	h0=dist.h0_mc(m, [zp[ind], ezp[ind]], 1000)
	
	print h0
	

main()

