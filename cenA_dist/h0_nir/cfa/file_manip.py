import numpy as np
import sys
import matplotlib.pyplot as plt

from pack import dist
def main():
    ff=np.loadtxt('f14_sne.tex', dtype='string', delimiter='&')
    z=ff[:,4].astype('float32')
    jmag=ff[:,8].astype('float32')
    err=ff[:,9].astype('float32')
    print jmag
    mu=np.array([dist.mod(i) for i in z])
    mjj=jmag-mu; mj2=mjj[(z>=0.01) & (err <=0.1)]
    print mu, np.std(mj2)
    
    plt.hist(mj2)
    plt.show()
#plt.hist(mjj)

main()