from numpy import loadtxt
from sys import argv
fout=open('tex/'+argv[1], 'w')
p=loadtxt('lit_t1.dat', dtype='string')
t2=loadtxt('../csp_sn/'+argv[3], dtype='string', usecols=(0, 1, 2))
ind=int(argv[2])
sn2=[i[4:len(i)] for i in t2[:,0]]
def r(k):
	return str(round(float(k), 2))
for i in p:
	fout.write(i[-1]+'\t&\t'+r(i[ind])+' $\pm$ '+r(i[3])+'\t&\t')
	fout.write(r(i[ind+1])+' $\pm$ '+r(i[ind+2])+'\t&\t\ldots\t&\t\ldots\t&\t')
	n=i[-1][0:len(i[-1])-1]
	if n in sn2:
		l1=sn2.index(n)
		fout.write(r(t2[l1][1])+' $\pm$ '+ r(t2[l1][2])+'\t&\t\ldots \\\\')
	else:
		fout.write('\t&\t\ldots \t&\t\ldots \\\\')
	fout.write('\n')
