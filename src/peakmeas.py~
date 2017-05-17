"""
Short script to interpolate the lbol-Mni relatino to get Mni for objects without u-H band coverage
"""
import numpy as np
import sys


from pack import bol



def main():
	#obtain peak bolometric flux
	bp=bol.bol_func().bolpeak
	
	#light curve file
	infile=sys.argv[1]
	lmax, t0, elmax=bp(infile)

	
	nivar=bol.model_comp().interp_mni
	bset=int(sys.argv[2])
	#print lmax, t0
	nimass=nivar(lmax/1e43, bset)
	print nimass
main()
	
