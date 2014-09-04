import numpy as np
import sys

rn=np.random.normal
vals=np.loadtxt('err_eqn_pap.txt', skiprows=1)
a=vals[2]
arr=[[a[1]*rn(a[2], a[3]), a[0]*rn(a[2], a[3])] for i in range(1000)]	#slope
arr1=[[a[1]*rn(a[4], a[5]), a[0]*rn(a[4], a[5])] for i in range(1000)]	#intercept
arr=np.array(arr);arr1=np.array(arr1)
ray=sys.argv[1]
if ray=='1':
	b=arr
else:
	b=arr1
ind=int(sys.argv[2])
print np.mean(b[:,ind]), np.std(b[:,ind])


