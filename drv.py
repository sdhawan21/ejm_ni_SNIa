#from mag2fl import *
from pandas import *
from matplotlib.pyplot import show
from scipy.interpolate import interp1d
from numpy import linspace, loadtxt, random
import bol_lc as bl
import math
import sys
t=loadtxt('mni_lcbol.txt', dtype='string')[:,0]
#print bl.lpeak_ni().ni_sn(sys.argv[1], 'BVRIJH')

class 
#h=loadtxt('lcbol_distrib/sn2007nq_lcbol_BVJ.dat', dtype='string')
'''
def sn_ni(obj):
	h=loadtxt('lcbol_distrib/sn'+obj+'_lcbol_BVJ.dat', skiprows=6)
	arr=[]
	for p in range(1000):
		sp=interp1d(h[:,0], random.normal(h[:,1], h[:,2]), kind='cubic') 
		l=linspace(min(h[:,0]), max(h[:,0]), 100)
		gp=sp(l)
		arr.append(max(gp))
	return mean(arr), std(arr)		
print sn_ni('2007nq')
'''
