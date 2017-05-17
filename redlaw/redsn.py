import numpy as np
import matplotlib.pyplot as plt

class redsn:
	tt=np.loadtxt('11fe_mags.txt', skiprows=1, usecols=(1, 2, 3))
	jcorr=tt[:,0]-28.91+27.64
	ax=tt[:,2]-jcorr
	plt.hist(ax, alpha=0.3)
	#plt.show()
print redsn().ax
	
