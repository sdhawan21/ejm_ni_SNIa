import numpy as np
import matplotlib.pyplot as plt
import sys

from pack import fid_time, bol
from scipy.optimize import curve_fit

bp = bol.bol_func().bolpeak
def read_lc(sn):
	f = '../test_'+sn+'_uvoir.txt'
	
	app_lc = np.loadtxt(f)
	alc = app_lc[app_lc[:,0].argsort()]
	print alc
	return alc
def abs_lc(sn, dm):
	"""
	shift to absolute flux
	"""
	lc = read_lc(sn)
	
	dl = pow(10,(dm - 25)/5.0)*3.08e24
	ar = 4*np.pi*dl**2
	
	lc[:,1]*=ar; lc[:,2]*=ar
	return lc

def shift_phase(sn, dm):
	"""
	Shift from the maximum
	"""
	alc = abs_lc(sn, dm)
	
	t = alc[alc[:,1]==max(alc[:,1])][0][0]#bp('../test_'+sn+'_uvoir.txt')[1]
	print t
	alc[:,0]-=t
	return alc
	
def main():
	sn = sys.argv[1]
	dm = float(sys.argv[2])
	rt = float(sys.argv[3])
	
	#define the filename
	f = '../test_'+sn+'_uvoir.txt'
	#mni = bp(f)[0]/2e43
	
	#shift to time of 
	lc = shift_phase(sn, dm)
	
	mni = max(lc[:,1])/(bol.arn_coef(rt)*1e43)
	
	print "The nickel mass is:", mni
	tail = lc[(lc[:,0] > 50) & (lc[:,0] < 100)]

	ft = fid_time.fid_time(mni)
	
	
	#shift to explosion date
	tail[:,0]+=rt
	
	t= np.linspace(0, 200, 500)
	p, c= curve_fit(ft.edp_nomc, tail[:,0], tail[:,1], p0=[30.])
	
	plt.errorbar(lc[:,0]+19, lc[:,1], lc[:,2], fmt= 'rs')
	plt.plot(t, ft.edp_nomc(t, p[0]))
	plt.show()
	print ft.ejm(p[0])
	print p
main()
