import numpy as np

import string as st
lc=np.loadtxt('raw/14j_opt.dat', dtype='string')
bands=['F336W', 'B', 'V', 'R', 'I']
fout=open('SN2014J_lc_bol.dat', 'w')

for k in bands:
	lcslice=lc[lc[:,1]==k][:, [0, 2, 3]]
	fout.write('#FILTER\t '+k+'_Bessell - '+str(len(lcslice))+' - MEASUREMENTS (MJD MAG MAGERR) \n')
	for j in lcslice:
		fout.write(j[0]+' '+j[1]+' '+str(float(j[2][1:-1])/1000.0)+'\n')
fout.close()
	
	
	