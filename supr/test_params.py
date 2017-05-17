import numpy as np
import sys
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d
from glob import glob

#shorthand for function
rn=np.random.normal
#path to dm15 values 
pt="/home/sdhawan/tests_paper/ni/files_snpy/"

def bolpeak(fil):
	lc=np.loadtxt(fil)
	ter=interp1d(lc[:,0], lc[:,1], kind='cubic')
	l=np.linspace(lc[:,0].min(), lc[:,0].max())
	gpl=ter(l)
	return max(gpl), l[gpl==max(gpl)][0]
def av_err(fil):
	fin=open(fil, 'r')
	ls=[]
	for row in fin:
		ls.append(row.split())
	return [ls[3][1], ls[4][3], ls[14][2]]
def err_bolpeak(fil):
	maxar=[]
	
	#take 1000 realisations of the light curve
	for k in range(1000):
		lc=np.loadtxt(fil)
		real=rn(lc[:,1], lc[:,2]) 
		
		#interpolation routine written within scipy, as Marco says "its fucknig amazing"
	
		ter=interp1d(lc[:,0], real, kind='cubic')
		l=np.linspace(lc[:,0].min(), lc[:,0].max())
		gpl=ter(l)
		maxar.append(max(gpl))
	
	return np.array(maxar)
def boots(arr):
	barr=[]
	for k in range(len(arr)):
		ind=int(np.random.uniform(0, 1)*len(arr))
		barr.append(arr[ind])
	return np.array(barr)
def ni_ddc(val):
	ddc=np.loadtxt('../comp_ddc/lpeak_m56ni.dat', usecols=(7, 1))
	tarr=[]
	for l in range(1000):
		ddc1=ddc
		#ddc1=boots(ddc)
		#ddc1=ddc1[ddc1[:,0].argsort()]
		#ddc1=np.unique(ddc1)
		#print ddc1
		err=np.random.uniform(0.0, 0.1, len(ddc1))
		real_X=rn(ddc1[:,0], np.ones(len(ddc1))*1e-10)
		spl=interp1d(real_X, rn(ddc1[:,1], err) , kind='cubic')
		l=np.linspace(real_X.min(), real_X.max())
		gpl=spl(l)
		l1=abs(l-val)
		tarr.append(gpl[l1==min(l1)][0])
	return np.array(tarr)
def rise_err(dm, lbol):
	"""
	
	calculate error in rise time by monte carlo 
	
	"""
	fac_arr=[]
	
	for k in range(10000):
	
		# Scalzo 2014 equation to cover the dm15-t,Rb locus of Ganeshalingham '11
		t=17.5-5*(rn(dm[0], dm[1])-1.1)
		
		# arnett's rule. Conservative 2 day uncertainty in rise time as in Scalzo 2014
		
		et=float(sys.argv[1])
		
		lb=6.45e43*np.exp(-rn(t, et)/8.8)+1.45e43*np.exp(-rn(t, et)/111.1)
		
		#normalize the coefficient
		fac=lb/1e43
		fac_arr.append(fac)
		
	return np.mean(fac_arr), np.std(fac_arr)

def err(x, y, sx):
	return sx/y 
	
	
def mbol(lbol):
	"""
	Convert bol luminosity to bolometric magnitude using solar references 
	"""
	return 4.8-np.log10(lbol*1e43/3.84e33)

def main():
	avarr=[]
	sset=sorted(glob('../lcbol_distrib/finfiles/*.dat'))
	for k in sset:
		avarr.append(av_err(k))
	print avarr
	return 0
	#infile, if from command line
	vals=np.loadtxt('../tables/u_flags.txt', usecols=(1, 2), skiprows=1)
	out=[]
	for i in vals:
		arr=ni_ddc(i[0])
		out.append([np.mean(arr), np.std(arr)])
	out=np.array(out)
	print out
	return 0
	#load the nickel mass estimates and the calculated bolometric luminosity
	rr=np.loadtxt("../tables/ni_dif.tex", dtype='string', usecols=(0, 1,2, 3), delimiter='&')
	
	
	
	#load Dm15 for variable rise calculation 
	dm=np.loadtxt(pt+"tmax_dm15.dat", dtype='string')
	
	#change name formats (remove the ' ' at the end)
	nm=[i[:-1] for i in rr[:,0]]; nm=np.array(nm)
	rr[:,0]=nm
	
	#create the arrays for the estimation using the err wala function re
	dmsamp=[[float(i[3]), float(i[4])] for i in dm if i[0] in rr[:,0]]
	lbol=[[float(rr[rr[:,0]==i[0]][0][1]), float(rr[rr[:,0]==i[0]][0][2])] for i in dm if i[0] in rr[:,0]]
	
	
	dmsamp=np.array(dmsamp); lbol=np.array(lbol)
	#coeffcients presuming alpha=1
	factot=[rise_err(dmsamp[i], lbol[i]) for i in range(len(dmsamp))]; factot=np.array(factot)
	
	#calculate the Ni masses
	z=lbol[:,0]/factot[:,0]
	
	#calculate the errors
	zerr=z*((lbol[:,1]/lbol[:,0])+(factot[:,1]/factot[:,0]))
	
	
	print  np.mean(factot[:,1]), np.mean(factot[:,0])
	
	#stop here for the error analysis
	return 0
	
	
	#does bolometric peak calculations 
	if len(sys.argv)==2:
		inf=sys.argv[1]

	sset=sorted(glob('../lcbol_distrib/finfiles/*.dat'))
	
	bp_arr=[]
	
	nmarr=[]
	
	#lbol=np.loadtxt('../tables/u_flags.txt', skiprows=1, usecols=(1, 2))
	
	for k in sset:
	
		bp=bolpeak(k)
	
		bp_arr.append(bp)
	
		nmarr.append([k, np.std(err_bolpeak(k)/1e43)])
	
	#return 0
	bp_arr=np.array(bp_arr)
	plt.hist(bp_arr/1e43, alpha=0.3)
	plt.hist(lbol[:,0], alpha=0.3)
	plt.show()
	
#main()
