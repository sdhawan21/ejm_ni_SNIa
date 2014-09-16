import funcs as fn
import mag2fl as mf
import numpy as np
barr=[i[0] for i in fn.pbin[:,0]]
flint=0
for m in barr:
    try:
        lc=mf.conv().rd_lc('SN2007on', m)
        f=np.zeros([len(lc['MJD']), 2]);f[:,0]=lc['MJD'];f[:,1]=lc[m]
        arfun=fn.flux_conv().all_time(f, m)
        flint+=fl_int(m)
        #print fn.interp().fl_int(arfun, 4)*fn.dist().mu2cm(31.45)
    except:
        m

#
