import numpy as np
import sys

from scipy.stats import pearsonr, kendalltau

def x1arr(arr, n):
	x1arr=[]; ex1arr=[]
	for i in arr:
		if n == 5 or n == 6:	
			try:
				a=-float(i[n][3:8])
				ea=float(i[n][9:-1])
			except:
				a=float(i[n][:5])
				ea=float(i[n][6:-1])		
			x1arr.append(a); ex1arr.append(ea)
		else:
			if n == 2:
				x1arr.append(float(i[n][:5]))
				ex1arr.append(float(i[n][6:-1]))
			else:
				x1arr.append(float(i[n][:6]))
				ex1arr.append(float(i[n][7:-1]))
	return x1arr, ex1arr
def main():
	arr=np.loadtxt('../ps1_csp_x1.dat', dtype='string')
	nm=arr[:,0]
	
	x1, ex1=x1arr(arr, 5)
	c, ec=x1arr(arr, 6)
	
	mb, emb=x1arr(arr, -3)
	z, ez=x1arr(arr, 2)
	
	out=np.vstack([nm, z, ez, mb, emb, x1, ex1, c, ec]).T
	np.savetxt("/home/sdhawan/workspaces/ic_proj/output_csp_r14.dat", out, fmt="%s")
main()
