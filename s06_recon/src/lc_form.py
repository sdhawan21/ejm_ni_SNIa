import numpy as np
import sys

filename = sys.argv[1]

try:
	lc=np.loadtxt(filename)
except:
	lc = np.loadtxt(filename, dtype='string')

out_lc = [] 

for i in lc:
	try:
		m1 = float(i[0])
		
		s = i[1][:6]+'e-'+i[1][-2:]
		s1 = i[2][:6]+'e-'+i[2][-2:]
		m2 = float(i[3])
		s2 = i[4][:6]+'e-'+i[4][-2:]
		s3 = i[5][:6]+'e-'+i[5][-2:]
		out_lc.append([m1, s, s1])
		out_lc.append([m2, s2, s3])
	except:
		i
np.savetxt('../test_'+filename[3:-8]+'_uvoir.txt', out_lc, fmt='%s')		
#arr=np.zeros([len(lc)*2, 3])
#for i in range(3):
#	a=np.concatenate([lc[:,0+i], lc[:,3+i]])
#	arr[:,i]=a
#print arr	
