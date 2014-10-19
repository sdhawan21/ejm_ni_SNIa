from sklearn.linear_model import RidgeCV, Ridge

import numpy as np
import matplotlib.pyplot as plt
rn=np.random.normal
uni=np.random.uniform
bvar=np.loadtxt('../../out_files/bivar_regress.txt', usecols=(1, 2, 3))

#run counter for if condition on y-band slope
i=0

val_arr=[]
coef_arr=[]
#start loop
while i<1000:
	ar=[]
	ar1=[]
	y=[]
	"""
	bootstrap sample the x and y arrays
	"""
	for l in range(len(bvar)):
		ind=int(uni(0, 1)*len(bvar))
		ar.append(bvar[ind][1])
		ar1.append(bvar[ind][2])
		y.append(bvar[ind][0])
	#write as arrays, stack them 
	ar=np.array(ar); ar1=np.array(ar1); y=np.array(y)
	A=np.vstack([ar, ar1, np.ones(len(bvar))]).T
	
	#cross-validate the ridge regression 
	cl=RidgeCV(alphas=[0.5, 1.0, 50.0, 500.0])
	#cl=Ridge(alpha=1.0)
	cl.fit(A, y)
	#if cl.coef_[0]>=0:
	i+=1

	#arrays for predicted values and for the a, b, c coefficients	
	val_arr.append(cl.predict([32.21, 31.01, 1.]))
	coef_arr.append([cl.coef_[0], cl.coef_[1], cl.intercept_])

print 'The mean and standard deviation for this object is '
print np.std(val_arr), np.mean(val_arr)
coef_arr=np.array(coef_arr)
print "Coefficients of the ridge and their standard deviations "
print np.mean(coef_arr[:,0]), np.std(coef_arr[:,0]), np.mean(coef_arr[:,1]), np.std(coef_arr[:,1]), np.mean(coef_arr[:,2]), np.std(coef_arr[:,2])

#plot the coefficient arrays
plt.hist(coef_arr[:,1], alpha=0.3)
plt.hist(coef_arr[:,0], alpha=0.3)
plt.show()
