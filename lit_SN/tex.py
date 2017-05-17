from numpy import loadtxt
from sys import argv
par=loadtxt('bn_params.txt',usecols=(0,1, 3, 4),  dtype='string')
fout=open(argv[1], 'w')
for i in par:
	for j in i:
		fout.write(j+'\t&\t')
	fout.write('\t\ldots\t&\t\ldots\t&\t\ldots \\\\ \n')
fout.close()

