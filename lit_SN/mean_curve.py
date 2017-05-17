from glob import glob 
#from ir_col import tmax
from sys import argv
from string import lower
from matplotlib.pyplot import errorbar, show
from numpy import loadtxt, mean, std
jsn=sorted(glob('fin_lc/'+lower(argv[1])+'_band/*'))
bn=sorted(glob('bn_ptf_sn/*'))
m_arr=[]
std_arr=[]
par=loadtxt('params.txt', dtype='string', skiprows=1)
bpar=loadtxt('bn_params.txt', dtype='string')
sn=par[:,0]
sn1=[i[4:len(i)] for i in sn ]
sn2=list(bpar[:,0])
print sn1
fout=open(argv[1]+'_mean_curve.dat', 'w')
ml=-10
t=int(argv[2])
for i in range(t):
	r_arr=[]
	for k in jsn:
		lc=loadtxt(k)
		if len(lc[:,0])>4:
			#print len(lc[:,0])
			s=k[14:len(k)-8]
			tm=float(par[sn1.index(s)][1])
			mu=float(par[sn1.index(s)][3])
			if min(lc[:,0])-tm-ml<1:
				ph=lc[:,0]-tm-ml
				mag=lc[:,1][list(abs(ph)).index(min(abs(ph)))]
				if mag<99:
					r_arr.append(mag-mu)
	for l in bn:
		if argv[1]=='J':
			lc=loadtxt(l, usecols=(0, 1, 3))
		elif argv[1]=='H':
			lc=loadtxt(l, usecols=(0, 4, 6))
		if len(lc[:,0])>2:
			#print len(lc[:,0])
			s=l[10:len(l)-4]
			tm=float(bpar[sn2.index(s)][1])
			mu=float(bpar[sn2.index(s)][4])
			if min(lc[:,0])-tm-ml<1:
				ph=lc[:,0]-tm-ml
				mag=lc[:,1][list(abs(ph)).index(min(abs(ph)))]
				if mag<99:
					r_arr.append(mag-mu)
	ml=ml+1
	if len(r_arr)>5:
		print mean(r_arr)
		m_arr.append(mean(r_arr))
		fout.write(str(ml)+'\t'+ str(mean(r_arr))+'\t'+str(std(r_arr))+'\n')
		std_arr.append(std(r_arr))

fout.close()		
