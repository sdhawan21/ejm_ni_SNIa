from numpy import loadtxt

fe=loadtxt('2011fe_IR.txt', dtype='string')
fout=open('phot_2011fe.txt', 'w')
tmax=55814.121
for i in fe:
	mjd=float(i[0])
	ph=mjd-tmax
	fout.write(str(ph)+'\t')
	for j in i:
		if j=='&':
			fout.write('\t')
		elif j[0]=='(':
			fout.write(j[1:len(j)-1]+'\t')
		elif j=='\\':
			fout.write('\t')
		else:
			fout.write('\t'+j+'\t')
	fout.write('\n')		