"""

Calculate transparency timescale (if Jeffrey 1999 equation isnt true then t0 can be covnerted to Mej as per what Wolfgang says)

"""

from mej_eq import mej
from test_params import bolpeak

from glob import glob


import numpy as np


edp=mej().edp
num=mej().numb

#number of seconds in a day
ds2=86400.0
#e-fold times for nickel and cobalt (56, resp.)			
lni=1/(8.8)
lco=1/(111.3)		

#Mev to ergs
fac=624150.647996

def t0_calc(arr):
	return arr
def main():
	sset=sorted(glob('../lcbol_distrib/finfiles/*.dat'))
	t0_arr=[]
	
	
	for k in sset:
		lc=np.loadtxt(k)
		tmax=bolpeak(k)[1]; ph=lc[:,0]-tmax
		mni=bolpeak(k)[0]/(2e43)
		nni=num(mni)
		
		ph1,mag1=mej().ran(ph, lc[:,1])
		
		l1=np.linspace(0, 40)
		edarr=[sum((mej().edp(ph1, nni, i)-mag1)**2) for i in l1]
		edarr=np.array(edarr)
		t0=l1[abs(edarr)==min(abs(edarr))][0]+19.0
		t0_arr.append([k[15:35], float(t0)])
	t0_arr=np.array(t0_arr)
	print t0_arr
main()
