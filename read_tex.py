import astropy.table as tb
import numpy as np
import sys
import matplotlib.pyplot as plt
import mag2fl as mf 
import bol_lc as bl

rd=bl.bol_lc().rd_bol


from scipy.stats import pearsonr
sys.path.append('../tests_paper/csp_sn/sec_max_files/')
pt=sys.path
class params:
	def rd_t2(self, fil):
		return np.loadtxt(pt[-1]+fil+'_sec_max_csp.dat', dtype='string')
	def arr(self, fil, ar1):
		return [float(i[1]) for i in self.rd_t2(fil) if 'sn'+i[0][2:len(i[0])] in ar1], [float(i[2]) for i in self.rd_t2(fil) if 'sn'+i[0][2:len(i[0])] in ar1]
	def a2(self, fil, ar):
		return [float() for i in self.rd_t2(fil) ]
'''
def main():
	op=np.loadtxt('m55_j.tex', delimiter='&', dtype='string')
	ni=np.loadtxt('mni_lcbol.txt', dtype='string', skiprows=1)
	ej=np.loadtxt('ejm_cur_dm.txt', dtype='string')
	k=params().arr('j', ej[:,0])
	drate=[float(i[1][1:-1]) for i in op if 'sn'+i[0][2:len(i[0])] in ej[:,0]]
	n=[float(ej[ej[:,0]=='sn'+i[2:len(i)]][0][1]) for i in params().rd_t2('j')[:,0] if 'sn'+i[2:len(i)] in ej[:,0]]
	en=[float(ni[ni[:,0]==i][0][2]) for i in params().rd_t2('j')[:,0] if 'sn'+i[2:len(i)] in ej[:,0]]
	print  len(n),  pearsonr(k[0], n)
	#plt.errorbar(k[0], n, xerr=k[1], yerr=en, fmt='r.')
	#plt.xlabel('$t_2$(J)')
	#plt.ylabel('$M_{ej}$')
	#plt.show()
	mn=ni[:,1].astype('float32')
	plt.hist(mn, alpha=0.4, color='g')
	u=np.loadtxt('snmcmc_results_runBp_mlo.txt', usecols=(16, 19))
	plt.hist(u[:,1], histtype='step', linewidth=3, color='b')
	#plt.show()
	#plt.hist(mn, histtype='step', color='r', linewidth=3)
	print pearsonr(n, drate)


main()
'''
class rt_bol:
	b14=np.loadtxt('burns14_ebv.tex', dtype='string', delimiter='&')
	def av_rv(self, sn, bands):
		fl=open('lcbol_distrib/'+sn+'_lcbol_'+bands+'.dat', 'r')
		ls=[]
		for row in fl:
			ls.append(row.split())
		b=self.b14
		print b[:,0]=='2004gs'#;sn[2:len(sn)]
		eb=float(b[b[:,0]==sn[2:len(sn)]][0][5][2:6])
		return float(ls[4][1]/ls[5][1]), eb  
if __name__ == '__main__':
	s=sys.argv[1]
	p=sys.argv[2]
	print rt_bol().av_rv(s, p)
	
	
	
	
	
