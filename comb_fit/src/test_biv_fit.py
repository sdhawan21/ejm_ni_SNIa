import numpy as np
import statsmodels.api as sm
import sys

#load output file with lbol, t2j, t2y
ff=np.loadtxt("../../out_files/bivar_regress.txt", usecols=( 1, 2, 3))

#ols framework


x=ff[:, [int(sys.argv[1]), int(sys.argv[2])]]
x=sm.add_constant(x)
res=sm.OLS(ff[:,2], x).fit()
print res.summary()



