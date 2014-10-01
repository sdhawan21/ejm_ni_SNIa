import numpy as np

from scipy.stats import pearsonr
pt='/home/sdhawan/tests_paper/csp_sn/sec_max_files/'
t=np.loadtxt('../tab_val.txt', delimiter='&', dtype='string')
p=np.loadtxt(pt+'j_sec_max_csp.dat', dtype='string')
t2=[float(i[1]) for i in t if i[0][0:-1] in p[:,0]  and float(i[4][3:6])+float(i[5][2:4]) < 0.1 ]
n=[float(p[p[:,0]==i[0]][0][1]) for i in t if i[0][0:-1] in p[:,0]  and float(i[4][3:6])+float(i[5][2:4]) < 0.1 ]

print pearsonr(t2, n)


