import numpy as np
import mag2fl as mf

import sys

from scipy.odr import *
from scipy.stats import pearsonr

rn=np.random.normal		#calculate the Mni estimate for the given value of t2 and t2err
pt='/home/sdhawan/tests_paper/csp_sn/sec_max_files/'
pt1='/home/sdhawan/bol_ni_ej/'
class  yjcorr:
	y=np.loadtxt(pt+'j_sec_max_csp.dat', dtype='string')		#load the two files for convenience
	j=np.loadtxt(pt+'y_sec_max_csp.dat', dtype='string')
	g=np.loadtxt(pt1+'uband_mni_nircorr.txt', dtype='string')	#bol_lum for measuring the correlation
	def f(self, B, x):
		return B[0]*x+B[1]	
	def int_band(self):		# for a single band, Ni mass estimates for the entire sample
		y1=self.y
		j1=self.j
		n=self.g
		t=[float(i[1]) for i in y1 if i[0] in j1[:,0] and i[0] in n[:,0]]
		tp=[float(j1[j1[:,0]==i[0]][0][1]) for i in y1 if i[0] in j1[:,0] and i[0] in n[:,0]]
		et=[float(i[2]) for i in y1 if i[0] in j1[:,0] and i[0] in n[:,0]]
		etp=[float(j1[j1[:,0]==i[0]][0][2]) for i in y1 if i[0] in j1[:,0] and i[0] in n[:,0]]
		nm=[i[0] for i in y1 if i[0] in j1[:,0] and i[0] in n[:,0]]
		rd=RealData(t, tp, sx=et, sy=etp)
		f1=Model(self.f)
		od=ODR(rd,f1,beta0=[1., 2.])
		out=od.run()
		t=np.array(t); et=np.array(et)
		res=[]
		for i in range(len(t)):
			p=[rn(out.beta[0], out.sd_beta[0])*rn(t[i], et[i])+rn(out.beta[1], out.sd_beta[1]) for k in range(1000)]
			res.append([nm[i], np.mean(p), np.std(p)])
		return np.array(res)
	def od_slp(self, a, b, c, d):		#odr libs to calculate relation for bf with errors
		rd=RealData(a, b, sx=c, sy=d)
		f1=Model(self.f)
		od=ODR(rd,f1,beta0=[1., 2.])
		out=od.run()
		return out.beta, out.sd_beta
		
def main():	
	ls=yjcorr().int_band()
	ni=yjcorr().g
	j=yjcorr().j
	n=[float(ni[ni[:,0]==i[0]][0][3]) for i in ls if i[0] in ni[:,0]]		#arrays for values and errors s
	w=[[float(i[1]) ,float(i[2])] for i in ls if i[0] in ni[:,0]]
	n1=[float(ni[ni[:,0]==i[0]][0][3]) for i in j if i[0] in ni[:,0]]
	w1=[[float(i[1]) ,float(i[2])] for i in j if i[0] in ni[:,0]]
	tni=np.concatenate([n, n1])
	t2=np.concatenate([w, w1])
	en=tni/3
	mn=t2[:,0]
	emn=t2[:,1]
	#print pearsonr(mn, tni)
	vals=yjcorr().od_slp(mn, tni, emn, en)
	bf=float(sys.argv[1]); er=float(sys.argv[2])
	ar=[rn(vals[0][0], vals[1][0])*rn(bf, er)+rn(vals[0][1], vals[1][1]) for k in range(1000)]	#mean and std for the Mni (14J, 06X, 86G etc.)
	print  vals, np.mean(ar), np.std(ar)
if len(sys.argv)==3:
	main()
else:
	print "Enter the t2 and t2_err for your objects of interest", "Usage: python \t"+sys.argv[0]+"\t<t2(days)> <err(days)>"
	
#np.savetxt('y2j.txt',ls, fmt='%s')
