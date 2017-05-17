import numpy as np
import matplotlib.pyplot as plt
import sys

#define paths:
ptphot='/home/sdhawan/RTN_SN_data/Photometry/'

optlc = np.loadtxt(ptphot+'Optical/2003hv_opt.dat', dtype='string', delimiter='&')

nirlc = np.loadtxt(ptphot+'NIR/2003hv_IR_early.dat', dtype='string')



#write the head of the file 
fout=open('2003hv_bol.dat', 'w')
fout.write(" #generated on Thu Oct 17 11:54:37 2013 using mklcbolinput.pro \n")
fout.write( " #NAME SN2003hv \n" )
fout.write(" #AV_HOST \t 0.05 +/- 0.003\n")
fout.write(" #RV_HOST 3.1 +/- 0.290\n")

fout.write("  #AV_MW \t 0.08 +/- 0.000 \n")
fout.write("#RV_MW  3.100 +/- 0.000\n")

fout.write("#DIST_MOD 31.45 +/- 0.1 \n") 
fout.write(" #NFILT  9")
fout.write("\n #\n")

filtarr_opt=['u', 'B', 'V', 'r', 'i']
filtarr_ir=['Y', 'J', 'H', 'K']

ph=optlc[:,2]
for k, filt in enumerate(filtarr_opt):
	mags = optlc[:, k+4]
	fout.write("#FILTER "+filt+"_CSP - "+str(len(mags)-10)+" MEASUREMENTS (MJD MAG MAGERR)\n")
	
	for j, ep in enumerate(ph):
		val = mags[j].strip()
		mval = val[:6]
		errval =  val[7:11]
		
		try:
			m=float(mval)
			fout.write(ep.strip()+' '+mval+' '+errval+'\n')
		except:
			ep

ph=nirlc[:,4]
for k, filt in enumerate(filtarr_ir):
	mags = nirlc[:, 2*k+7]; errs=nirlc[:,2*k+8]
	fout.write("#FILTER "+filt+"_CSP - "+str(len(mags))+" MEASUREMENTS (MJD MAG MAGERR)\n")
	
	for j, ep in enumerate(ph):
		mval = mags[j].strip()
		#mval = val[:6]
		#errval =  val[7:11]
		errval=errs[j].strip()
		try:
			m=float(mval)
			if m < 40:
				fout.write(ep+' '+mval+' '+errval+'\n')
		except:
			ep
	
fout.close()
