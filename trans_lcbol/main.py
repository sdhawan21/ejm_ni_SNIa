import funcs as fn
import mag2fl as mf
import numpy as np
import sys

"""
define command line inputs: SN name, distance modulus
"""

sn=sys.argv[2]
dinp=float(sys.argv[3])

#define bands

barr=[i[0] for i in fn.pbin[:,0]]


lc=mf.conv().rd_lc(sn, barr[1])
flint=np.zeros(len(lc['MJD']))
for k in range(len(barr)-1):
    try:
    	lc=mf.conv().rd_lc(sn, barr[k]); f=np.zeros([len(lc["MJD"]), 2])
    	f[:,0]=lc["MJD"];f[:,1]=lc[barr[k]]
    	fn.flux_conv().all_time(f, barr[k])
    	flint+=fn.interp().fl_int(f, 1, barr[k])
    except:
    	barr[k]
dis=fn.dist().mu2cm(dinp)
print flint*dis
