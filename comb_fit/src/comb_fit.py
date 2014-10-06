import statsmodels.api as sm
import numpy as np

from sklearn import linear_model

#define path to the second maximum files

pt='/home/sdhawan/tests_paper/csp_sn/sec_max_files/'

#function to define arrays
def arr_def():
	#load the x1, x2, y files
	jb=np.loadtxt(pt+'j_sec_max_csp.dat', dtype='string')
	yb=np.loadtxt(pt+'y_sec_max_csp.dat', dtype='string')
	fl=np.loadtxt('../../tables/u_flags.txt', dtype='string')
	
	#define the arrays
	lb=np.array([float(i[1]) for i in fl if i[0] in jb[:,0] and i[0] in yb[:,0]])
	yt2=[float(yb[yb[:,0]==i[0]][0][1]) for i in fl if i[0] in jb[:,0] and i[0] in yb[:,0]]
	jt2=[float(jb[jb[:,0]==i[0]][0][1]) for i in fl if i[0] in jb[:,0] and i[0] in yb[:,0]]
	
	#stack arrays in a shape that is readable by sm modules
	x1=np.vstack([yt2, jt2]).T
	x=np.vstack([x1[:,0], x1[:,1], np.ones(len(yt2))]).T
	x=x[:10]; lb=lb[:10]
	x=sm.add_constant(x)
	
	#perform regression
	est=sm.OLS(lb, x).fit()
	
	return est
def main():
	est=arr_def()
	print est.summary()
main()
