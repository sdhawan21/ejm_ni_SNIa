import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm


from matplotlib.ticker import MultipleLocator
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from string import upper
from scipy.stats import pearsonr


fp=FontProperties(family='times new roman', size=25)
inp=np.loadtxt("vals.txt")
"""
first function deals with plotting the histogram for the different methods
"""
def plot_hist():
	
	plt.rcParams['axes.linewidth']=2.5
	
	plt.rcParams['xtick.major.pad']=8
	plt.rcParams['ytick.major.pad']=8
	#ni3=np.array([float(i[3][:-3]) for i in inp])
	
	#inp[:,3]=ni3; inp[:,1].astype('float32'); inp[:,2].astype('float32')
	#for the 3 filters, it plots the arrays with mpl libs
	fig=plt.figure(figsize=(15, 18))		
	fil=['y', 'j', 'h']
	s=[311,312,310]
	f=['y', 'g', 'r']
	lablist=["var", "fixed", "DDC"]
	for k in range(3):
		print k
		sp=plt.subplot(s[k])
		sp.minorticks_on()
           	sp.tick_params('both', length=15, width=2)
           	sp.tick_params('both', length=7, width=2, which='minor')
		plt.xlim(0.2, 0.8)
		plt.ylim(0.0, 8.0)
	   	frame=plt.gca()
	   	sp.yaxis.set_major_locator(MultipleLocator(3))
	   	ytickar=frame.axes.get_yticklabels()
	   	
	   	for ylab in ytickar:
	   	#if ylab!=ytickar[0]: #and ylab !=ytickar[-1]:
	   		ylab.set_fontproperties(fp) 
	   	#else:
	   	#	ylab.set_visible(False)
		#	ylab.set_fontsize(0.0)
	   	ytickar[0].set_visible(False); ytickar[-1].set_visible(False)
	   	if s[k]!=310:
			for xlab in frame.axes.get_xticklabels():
				xlab.set_visible(False)
				xlab.set_fontsize(0.0)
	   	else:
	   		for xlab in frame.axes.get_xticklabels():
	   			xlab.set_fontproperties(fp) 
		plt.hist(inp[:,k], color=f[k], bins=np.arange(0.2, 0.8, 0.1), label=lablist[k], histtype='step', linewidth=2)
		plt.legend(loc=2, prop={'size':35})
		
	plt.subplots_adjust(hspace=0)
	plt.xlabel('$M_{^{56}Ni}$', fontsize=45, labelpad=10)
	plt.subplot(312)
	plt.ylabel('$N_{SN}$', fontsize=45, labelpad=10)
	plt.savefig('hist_ni.pdf')	
def plot_line():
	er=np.loadtxt('vals_tab.tex', usecols=(1, 2), delimiter='&')[:,1]
	plt.rcParams['axes.linewidth']=2.5
	
	plt.rcParams['xtick.major.pad']=7
	plt.rcParams['ytick.major.pad']=7
	#ni3=np.array([float(i[3][:-3]) for i in inp])
	
	#inp[:,3]=ni3; inp[:,1].astype('float32'); inp[:,2].astype('float32')
	#for the 3 filters, it plots the arrays with mpl libs
	fig=plt.figure(figsize=(12, 18))		
	fil=['y', 'j', 'h']
	s=[211, 210]
	f=['yD', 'rs']
	lablist=["var", "DDC"]
	arr=[0, 2]
	for k in range(2):
		print k
		sp=plt.subplot(s[k])
		sp.minorticks_on()
           	sp.tick_params('both', length=15, width=2)
           	sp.tick_params('both', length=7, width=2, which='minor')
		plt.xlim(0.2, 0.8)
	   	plt.ylim(-0.3, 0.3)
	   	frame=plt.gca()
	   	ytickar=frame.axes.get_yticklabels()
	   	
	   	for ylab in ytickar:
	 
	   		ylab.set_fontproperties(fp) 
	   		
	   	ytickar[0].set_visible(False) 
	   	ytickar[-1].set_visible(False)
	   	if s[k]!=210:
			for xlab in frame.axes.get_xticklabels():
				xlab.set_visible(False)
				xlab.set_fontsize(0.0)
	   	else:
	   		for xlab in frame.axes.get_xticklabels():
	   			xlab.set_fontproperties(fp) 
	   	dif=inp[:,arr[k]]-inp[:,1]
	   	
	   	print pearsonr(dif, inp[:,1])
	   	
	   	res=sm.OLS(dif, inp[:,1]).fit()
	   	
	   	print res.predict(0.7), er
		plt.errorbar(inp[:,1], dif, er, fmt=f[k], ms=15, linewidth=2.5, label=lablist[k])
		plt.legend(loc=2, numpoints=1, prop={'size':35})
		plt.ylabel('$Diff$', fontsize=35, labelpad=4)
	
	
	plt.subplots_adjust(hspace=0)
	plt.xlabel('$M_{^{56}Ni}(fixed)$', fontsize=30, labelpad=7)
	plt.savefig('dif_ni_comp.pdf')

def lmax_scat():
	plt.rcParams['axes.linewidth']=2.5
	
	plt.rcParams['xtick.major.pad']=9
	plt.rcParams['ytick.major.pad']=6
	fig=plt.figure(figsize=(12, 18))		
	fil=['y', 'j']
	s=[211, 210]
	f=['yD', 'rs']
	lablist=["Arnett-var", "DDC"]
	arr=[0, 2]
	iny_files=np.loadtxt('../../out_files/new_lbolhist_y.txt', dtype='string')
	inj_file=np.loadtxt('../../out_files/new_lbolhist_j.txt', dtype='string')
	
	print inj_file
	
	dif=[float(inj_file[inj_file[:,0]==i[0]][0][1])-float(i[1]) for i in iny_files if i[0] in inj_file[:,0]]	
	lmaxj=[float(inj_file[inj_file[:,0]==i[0]][0][1]) for i in iny_files if i[0] in inj_file[:,0]]	
	elm=[float(inj_file[inj_file[:,0]==i[0]][0][2]) for i in iny_files if i[0] in inj_file[:,0]]
	edif=[float(inj_file[inj_file[:,0]==i[0]][0][2])+float(i[2]) for i in iny_files if i[0] in inj_file[:,0]]
	
	sp=plt.subplot(111)
	sp.minorticks_on()
      	sp.tick_params('both', length=15, width=2)
       	sp.tick_params('both', length=7, width=2, which='minor')
	plt.xlim(0.6, 1.6)
   	plt.errorbar(lmaxj, dif, xerr=elm, yerr=edif, fmt='rs', ms=15, linewidth=2.5)
   	frame=plt.gca()
   	ytickar=frame.axes.get_yticklabels()
   	xtickar=frame.axes.get_xticklabels()
   	for ylab in ytickar:
 		if ylab != ytickar[0]:
 	  		ylab.set_fontproperties(fp) 
   	for xlab in xtickar:
 
   		xlab.set_fontproperties(fp)
   		
   	ytickar[0].set_visible(False)
   	xtickar[0].set_visible(False)
   	plt.ylabel('$L_{max}$(J)-$L_{max}$(Y)', fontsize=35, labelpad=5)
   	plt.xlabel('$L_{max}(J)$',  fontsize=35, labelpad=5)
	plt.savefig('lmax_scat.pdf')

def  lmax_est_hist():
	filt=['y', 'j']
	c=['y', 'g']
	s=[211, 210]
	fig=plt.figure(figsize=(12, 18))
	plt.rcParams['axes.linewidth']=2.5
	
	plt.rcParams['xtick.major.pad']=9
	plt.rcParams['ytick.major.pad']=6
	for k in range(2):
		infile=np.loadtxt('../../out_files/new_lbolhist_'+filt[k]+'.txt', usecols=(2, 1))
		sp=plt.subplot(s[k])
		sp.minorticks_on()
           	sp.tick_params('both', length=15, width=2)
           	sp.tick_params('both', length=7, width=2, which='minor')
		plt.xlim(0.6, 1.6)
		plt.ylim(0.0, 10.0)
	   	frame=plt.gca()
	   	sp.yaxis.set_major_locator(MultipleLocator(3))
	   	ytickar=frame.axes.get_yticklabels()
	   	
	   	for ylab in ytickar:
	 
	   		ylab.set_fontproperties(fp) 
	   		
	   	#ytickar[0].set_visible(False)
	   	if s[k]!=210:
			for xlab in frame.axes.get_xticklabels():
				xlab.set_visible(False)
				xlab.set_fontsize(0.0)
	   	else:
	   		for xlab in frame.axes.get_xticklabels():
	   			xlab.set_fontproperties(fp) 
		plt.hist(infile[:,1], color=c[k], bins=np.arange(0.6, 1.6, 0.1))
		plt.annotate(upper(filt[k]),xy=(0.1, 0.8), xycoords="axes fraction", fontsize=35, weight='bold')
		plt.ylabel('$N_{SN}$', fontsize=35)
	plt.xlabel('$L_{max}$', fontsize=35)
	plt.subplots_adjust(hspace=0)	
	plt.savefig('lmax_est_hist.pdf')
			
def main():
	plot_line()
	plot_hist()
	#lmax_scat()
	#lmax_est_hist()
main()
