import numpy as np
import sys
import matplotlib.pyplot as plt

#opt=np.loadtxt('raw_iptf13ebh_opt.dat', dtype='string')
#ir = np.loadtxt('raw_iptf13ebh.dat', dtype='string')

opt=np.loadtxt('raw_99by_opt.dat', dtype='string')
ir = np.loadtxt('raw_99by.dat', dtype='string')
#fout = open('iptf13ebh_bol.dat', 'w')
fout = open('99by_bol.dat', 'w')
#opt_filt = ['B', 'V', 'u', 'g', 'r', 'i']
opt_filt=['U', 'B', 'V', 'R', 'I']

#ir_filt = ['Y', 'J', 'H']
ir_filt = [ 'J', 'H', 'K']

fout.write(" #generated on Thu Oct 17 11:54:37 2013 using mklcbolinput.pro \n")
fout.write( " #NAME  SN1999by \n" )
fout.write(" #AV_HOST \t 0.15 +/- 0.06  \n")
fout.write(" #RV_HOST \t 3.1 +/- 0.290\n")
fout.write("  #AV_MW \t 0.207 +/- 0.000 \n")
fout.write("#RV_MW  3.100 +/- 0.000\n")
fout.write("#DIST_MOD 33.63 +/- 0.18 \n") 
fout.write(" #NFILT "+str(len(opt_filt+ir_filt)))
fout.write("\n #\n")

for  i, filt in enumerate(opt_filt):
	indexx = (i)*2+1
	print i
	lc=opt[:,[0, indexx, indexx+1]]
	#print lc
	lc1=lc[lc[:,1]!='99']
	meas=len(lc1)
	fout.write("#FILTER "+filt+"_Bessell - "+str(meas)+"  MEASUREMENTS (MJD MAG MAGERR)\n")
	for ll in range(len(lc1)):
		fout.write(str(lc1[ll][0])+' '+str(lc1[ll][1])+' 0.'+str(lc1[ll][2][1:-1])+'\n')


for  i, filt in enumerate(ir_filt):
	indexx = (i)*2+1
	lc=ir[:,[0, indexx, indexx+1]]
	#print lc
	lc1=lc[lc[:,1]!='99']
	meas=len(lc1)
	fout.write("#FILTER "+filt+"_MKO - "+str(meas)+"  MEASUREMENTS (MJD MAG MAGERR)\n")
	for ll in range(len(lc1)):
		fout.write(str(lc1[ll][0])+' '+str(lc1[ll][1])+' '+str(lc1[ll][2][1:-1])+'\n')
fout.close()
