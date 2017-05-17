"""
Calculate the absorption law for SNe~Ia without the use of multicolor light curves 
-Comparison to Power law (amanullah '14 and Goobar '08)
-Cardelli law with calculated RV
-Cardelli law with RV=1.7 (Phillips 2012)

Prints: Rv, e_Rv, A_v
Returns: A_v (meas) versus A_v literature
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import powerlaw

from scipy.stats import pearsonr, chisquare
from scipy.odr import *
from pack import dist

rn=np.random.normal

def corrcoeff(peakall, col, rlam, t2):
    peak=peakall[:,col]-np.array([dist.mod(i[0])+rlam*i[-1] for i in peakall])
    t=t2[:,0]#; print pearsonr(peak, t)
    rd=RealData(t, peak)
    def f(B, x):
        return B[0]*x+B[1]
    f=Model(f)
    od=ODR(rd, f, beta0=[1., 2.])
    out=od.run()
    return out.beta, out.sd_beta

def mtrue(peakall, col, rlam, t2, val=[31.99, 1.1]):
	v, ev=corrcoeff(peakall, col, rlam, t2)

	ar=[rn(v[0], ev[0])*rn(val[0], val[1])+rn(v[1], ev[1]) for k in range(10000)]

	return np.mean(ar), np.std(ar)	
dis=np.loadtxt('../csp_dist.txt', dtype='string')
mags=np.loadtxt('mags_sne.txt', dtype='string')

def calcvals(sn, tval, etval):
	"""
	estimate the A_v from the observed mag and the t2
	"""

	#load  calibration sample files

	t2=np.loadtxt('t2_forcorr.txt', usecols=(1, 2))
	peakall=np.loadtxt('allpeaks.txt', usecols=(1, 2, 3, 4, 5,6,7, 8))	
	#peakall=peakall[peakall[:,0]>0.01]; t2=t2[peakall[:,0]>0.01]
	col_range=range(1, 7)
	#define MW R_X values and central wavelength
	rlamarr=[4.1, 3.1,2.7,2.08, 0.89, 0.57]
	lamarr=np.array([.4, .53, .6, .8, 1.2, 1.6])
	
	inv_lam=1./lamarr		

	#print rlamarr
	
	#calculate the inferred magnitudes
	mag14j=np.array([mtrue(peakall, i, rlamarr[i-1], t2, val=[tval, etval]) for i in col_range])

	mag14j=np.array(mag14j)

	mu=float(dis[dis[:,0]==sn][0][1]) 

	obsmag=mags[mags[:,0]==sn][0][1:]; obsmag=obsmag.astype('float32')

	obsabsmag=obsmag-mu
	
	abs_filt=obsabsmag-mag14j[:,0]
	ext=-abs_filt+ abs_filt[1]
	

	rv= -abs_filt[1]/ext[0]
	print "R_v is:", rv
	print "Error is:", mag14j[1][1]	

	print "A_v is:", abs_filt[1]
	lamspace=np.linspace(0.3, 1.7)
	pl_abs=abs_filt[1]*pow((.53/lamspace), 2.1)

	invspace= 1./lamspace
	am14_ext= -pl_abs + abs_filt[1]
	
	pl_nospace_abs=abs_filt[1]*pow((.53/lamarr), 2.1)
	am14_nospace_ext=-pl_nospace_abs + abs_filt[1]	

	card=np.loadtxt('relations/card_coef.txt', skiprows=1, usecols=(1, 2))

	al_av= card[:,0] + card[:,1]/rv
	card_ext= -((al_av) * (abs_filt[1])) + abs_filt[1]

	

	#print am14_ext, ext

	
	#plot the observed extinction along with reddening laws	
	#plt.plot(invspace , am14_ext, label='Amanullah Power Law')
	#plt.errorbar(inv_lam, ext, mag14j[:,1]+0.15,  fmt='r.', label='Inferred Absorptions')
	#plt.plot(inv_lam, (-1.88*(.4/inv_lam)**3) + 1.88)	
	al_av1_7= card[:,0] + card[:,1]/1.7
	
	card_ext1_7= -((al_av1_7) * (abs_filt[1])) + abs_filt[1]
	
	cext=[card_ext[i] for i in [0,  2,3, 4, 5]]
	am_ext=[am14_nospace_ext[i] for i in [0,  2,3, 4,5]]
	et=[ext[i] for  i in [0,  2,3,4, 5]]
	#print et, am_ext, cext	
	#calculate the chi-sq statistic
	chsq_card= chisquare(et, cext)[0]
	chsq_am=chisquare(et, am_ext)[0]
	
	 
	print "Chisq for card:", abs(chsq_card)
	print "Chisq for power law:", abs(chsq_am)

	return abs_filt[1], mag14j[1][1]+0.15
	
	plt.plot(inv_lam, card_ext, label='CCM '+str(rv))
	plt.plot(inv_lam, card_ext1_7, label='CCM RV=1.7')


	plt.xlim(0.4, 3)
	plt.xlabel('1/$\lambda$ (1/$\mu$m)')
	plt.ylabel('E(V-X)')

	plt.legend(loc=0)
	plt.show()

def main():
	"""
	Use the absorption values from Burns' 2014, compare to estimates from the t_2 method
	"""
	avfile=np.loadtxt('avval_lit.txt', dtype='string')
	

	if len(sys.argv)==2:
		sn=sys.argv[1]
	elif len(sys.argv) ==4 :	
		sn=sys.argv[1]; tval=float(sys.argv[2]); etval=float(sys.argv[3])
	else:
		avcomp=[]
		t2file=np.loadtxt('/Users/lapguest/csp_sn/sec_max_files/j_sec_max_csp.dat', dtype='string')
		for i in t2file:
			try:
				sn=i[0]
				
				tval=float(i[1])
				etval=float(i[2])
				litav=float(avfile[avfile[:,0]==sn][0][1]); e_litav=float(avfile[avfile[:,0]==sn][0][2])
				
				av, e_av=calcvals(sn, tval, etval)
				
				avcomp.append([av, e_av, litav, e_litav])		
			except:
				i[0]
			
		avcomp=np.array(avcomp)
		#avcomp=avcomp[avcomp[:,2]>.6]			
		print pearsonr(avcomp[:,0], avcomp[:,2])	
		print "Total number of SNe is:", len(avcomp)
		plt.errorbar(avcomp[:,0], avcomp[:,2], xerr=avcomp[:,1], yerr=avcomp[:,3], fmt='g^')
		plt.plot([-0.5, 9], [-0.5, 9], 'k:')
		plt.xlabel('$A_V (measured)$')
		plt.ylabel('$A_V (lit)$')
		plt.show()

main()
	
