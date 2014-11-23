import funcs as fn	#in same direc
import mag2fl as mf	#added to pythonpath (must do same on any other pc)	
import numpy as np
import sys
import matplotlib.pyplot as plt


"""
define command line inputs: SN name, distance modulus
"""

sn=sys.argv[2]
dinp=float(sys.argv[3])

#define bands
def main():
	#filters 
	barr=[i[0] for i in fn.pbin[:,0]]

	#light curve for first band
	lc=mf.conv().rd_lc(sn, barr[1])
	flint=np.zeros(len(lc['MJD']))
	
	for k in range(len(barr)-1):
	    try:
	    	#read in k'th band data
	    	lc=mf.conv().rd_lc(sn, barr[k])
	    	f=np.zeros([len(lc["MJD"]), 2])
	    	
	    	#put light curve in the empty array
	    	f[:,0]=lc["MJD"];f[:,1]=lc[barr[k]]
	    	
	    	
	    	fn.flux_conv().all_time(f, barr[k])
	    	flint+=fn.interp().fl_int(f, 1, barr[k])
	    except:
	    	barr[k]
	dis=fn.dist().mu2cm(dinp)
	
	absfl=flint*dis
	plt.plot(absfl, 'r.')
	plt.show()
	#print flint*dis
if len(sys.argv)==4:
	main()
else:
	print "Usage: python"+sys.argv[0]+'<band> <sn> <distance modulus>'
