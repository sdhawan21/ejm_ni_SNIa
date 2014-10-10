from sklearn.decomposition import PCA

import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt

rn=np.random.normal

def pca_trans(arr):
	pca=PCA(n_components=1)
	pca.fit(arr)

	return pca.transform(arr)
def boots(arr, nsamp=1000):
	mean_ar=[]
	for num in range(nsamp):
		ar=[]
		for k in range(len(arr)):
			ind=int(len(arr)*np.random.uniform(0, 1))
			ar.append(arr[ind])
		mean_ar.append(np.mean(ar))
	return mean_ar
def main():
	
	inp=np.loadtxt('../../out_files/bivar_regress.txt', usecols=(1, 2, 3))

	X=inp[:,[1, 2]]
	
	pca=PCA(n_components=1)

	pca.fit(X)
	
	l=pca.transform(X)

	#l[:,0]-=pca.mean_[0]
	
	#l[:,1]-=pca.mean_[1]
	
	res=sm.OLS(inp[:,0], l).fit()
	
	print res.summary(), np.std([rn(-0.0264, 0.004)*pca.transform(rn(31.01, 0.31))+np.mean(inp[:,0]) for k in range(1000)]), np.std(inp[:,0])/np.sqrt(len(inp[:,0])), np.std(boots(inp[:,0]))


main()







