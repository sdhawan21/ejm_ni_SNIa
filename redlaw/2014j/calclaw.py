import numpy as np
import matplotlib.pyplot as plt
import sys

def powlaw(lam, av=[1.88, 0.1]):
	alam=av[0]* pow((.4/lam), 2.1) 
	return alam
def main():
	av=[1.88, 0.1]
	lamarr=[0.4, 0.53, 0.6, 0.8, 1.2, 1.6]
	lamarr=np.array(lamarr)	
	print lamarr
	alam=[powlaw(i) for i in lamarr]; alam=np.array(alam)

	ext=-alam+av[0]
	print ext
	inv_lam= 1./lamarr

	plt.plot(inv_lam, ext, 'b.')
	#plt.show()
main()






