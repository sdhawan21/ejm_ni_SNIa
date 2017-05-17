import numpy as np
import matplotlib.pyplot as plt

from astropy.io import ascii
pt='/home/sdhawan/tests_paper/csp_sn/sec_max_files/'
inp=np.loadtxt('../test/lrtest.tex', delimiter='&', dtype='string')
def add_col():
	aa=[]
	ht2=np.loadtxt(pt+'h_sec_max_csp.dat', dtype='string')
	for i in inp:
		nm=i[0][:-1]
		if nm in ht2[:,0]:	
			val=str(round(float(ht2[ht2[:,0]==nm][0][1]), 1)) 
			err=str(round(float(ht2[ht2[:,0]==nm][0][2]), 1)) 
			aa.append(val+'\t $\pm$ \t'+err) 
		else:
			aa.append('\ldots')
	aa=np.array(aa)
	return aa
def main():
	all_arr=[]
	nc=add_col()
	for i in range(len(inp)):
		r=[]
		for j in range(6):
			r.append(inp[i][j])
		r.append(inp[i][7][:-2]+'\t')
		r.append(inp[i][6]+'\t')
		r.append(nc[i]+'\t \\\\')
		all_arr.append(r)
	np.savetxt('../out_files/tab1.tex', all_arr,fmt='%s', delimiter='&')
main()
