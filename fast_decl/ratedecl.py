import numpy as np
import matplotlib.pyplot as plt
import sys

from pack import bol

def main():	
	bp=bol.bol_func().bolpeak
	infile=sys.argv[1]
	lc=np.loadtxt(infile)
	peak=bp(infile)
	lc[:,0]-=peak[1]
	lc[:,1]=lc[:,1]/1e43
	lc[:,1]=-2.5*np.log10(lc[:,1])
	
	plt.plot(lc[:,0], lc[:,1], 'g^')
	
	dec=bol.bol_func().late_decl
	m,c=dec(lc, ran=[30, 90])
	print "the slope is", m
	plt.show()
main()
