from numpy import loadtxt
from sys import argv
from glob import glob
#snls=glob(argv[1]+'_ir.ascii')
#snls=snls.remove('99ee_ir.ascii')
a=int(argv[2])
c=int(argv[3])
e=int(argv[4])
b=['b', 'v', 'r', 'i', 'j', 'h']
k=int(argv[5])
l=argv[1]
#for l in snls:
lc=loadtxt(l, usecols=(e,a,c), dtype='string')
fout=open(argv[6]+'_band/'+k+'_'+argv[6]+'.ascii', 'w')
for i in lc:
	for j in i:
		fout.write(j+'\t')
	fout.write('\n')
fout.close()
