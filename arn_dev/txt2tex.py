import sys



fl=sys.argv[1]
f1=open(fl, 'r')
ff=fl[:-3]+'tex'
fout=open(ff, 'w')
ls=[]
for row in f1:
	ls.append(row.split())
for k in ls:
	for j in k:
		if j != k[-1]:
			fout.write(j+'\t&\t')
		else:
			fout.write(j+'\t')
	fout.write('\\\\\n')
			