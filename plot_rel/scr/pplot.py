"""
--> Script to plot the first figure of Paper II (electric boogaloo? sheeessh!)

it plots the main correlatino between Lmax and t2 in YJH. 
(seems to be a  Bruno-approved template of the plot)
"""
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import MultipleLocator
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from string import upper
from scipy.stats import pearsonr

from pack import bol

fp=FontProperties(family='times new roman', size=30)

#define paths 
pt='/home/sdhawan/tests_paper/csp_sn/sec_max_files/'
pt1='/home/sdhawan/bol_ni_ej/'

def arr(bd):								
	#creates the arrays from the files (using simple if conditions)
	
	#lbol file
	uir=np.loadtxt(pt1+'tables/u_flags.txt', dtype='string', skiprows=1)
	uir=uir[uir[:,3]=='UBVRIJH']
	#t2 files 
	t2=np.loadtxt(pt+bd+'_sec_max_csp.dat', dtype='string')
	t=[float(i[1]) for i in t2 if i[0] in uir[:,0]]
	ni=[float(uir[uir[:,0]==i[0]][0][1]) for i in t2 if i[0] in uir[:,0]]
	ne=[float(uir[uir[:,0]==i[0]][0][2]) for i in t2 if i[0] in uir[:,0]]
	et=[float(i[2]) for i in t2 if i[0] in uir[:,0]]
	nm=[i[0] for i in t2 if i[0] in uir[:,0]]
	return t, ni, ne, et, nm
def main():
	#use rcParams to get better definitions of the axes widths 
	plt.rcParams['axes.linewidth']=2.5
	
	plt.rcParams['xtick.major.pad']=8
	plt.rcParams['ytick.major.pad']=8

	#for the 3 filters, it plots the arrays with mpl libs
	
	fig=plt.figure(figsize=(12, 18))		
	fil=['y', 'j', 'h']
	s=[311,312,310]
	f=['yD', 'g.', 'rs']
	#corr=[[0.04, -0.055],[0.042, -0.039],[0.033, -0.239]]
	for i in range(3):
           
           #plot details
           
           sp=plt.subplot(s[i])
           sp.minorticks_on()
           sp.tick_params('both', length=15, width=2)
           sp.tick_params('both', length=7, width=2, which='minor')
	   plt.xlim(10, 40)
	   plt.ylim(0.4, 1.8)
	   frame=plt.gca()
	   ytickar=frame.axes.get_yticklabels()
	   print ytickar
	   for ylab in ytickar:
	   	#if ylab!=ytickar[0]: #and ylab !=ytickar[-1]:
	   	ylab.set_fontproperties(fp) 
	   	#else:
	   	#	ylab.set_visible(False)
		#	ylab.set_fontsize(0.0)
	   ytickar[0].set_visible(False)
	   ytickar[-1].set_visible(False)
	   print np.shape(ytickar), ytickar[0]
	   
	   #remove the ticklabels from the x-axes
	   if s[i]!=310:
		for xlab in frame.axes.get_xticklabels():
			xlab.set_visible(False)
			xlab.set_fontsize(0.0)
	   else:
	   	for xlab in frame.axes.get_xticklabels():
	   		xlab.set_fontproperties(fp)
	   		
	   #use the array creating function to get the four arrays out 	   	
	   t,n,ne,et, nm=arr(fil[i])
	   #print pearson coefficient as a sanity check
	   print pearsonr(t,n)
	   #actually do the plotting
	   plt.errorbar(t, n, xerr=et, yerr=ne, fmt=f[i], ms=15, elinewidth=2.5)
	   t=np.array(t)
	   
	   #vs=np.vstack([t, np.ones(len(t))]).T; a=np.linalg.lstsq(vs, n)[0] #print a, len(t)		#calculates the best fit linear model

	   #vertically stack all the arrays
	   vs1=np.array([nm, t, et, n, ne]).T
	   vs=np.array([ t, et, n, ne]).T
	   np.savetxt('lbol_t2_'+fil[i]+'.txt', vs1, fmt='%s')
	   a, b=bol.linfits().freq_odr(vs)
	   #print slope and intercept along with the errors (m,c, dm, dc)
	   print a, b

	   #overplot best fit
	   plt.plot(t, a[0]*t+a[1], 'k:', linewidth=2.5)
	   
	   #annotate the filter id
	   plt.annotate(upper(fil[i]), xy=(0.1, 0.85), xycoords="axes fraction", fontsize=30, weight='bold')
	#frame=gca()
	#if s[i]!=310:
		#frame.xticklabels()
	#labels and adjust white space between the subplots 
	plt.subplots_adjust(hspace=0)
	plt.xlabel('$t_2(days)$', fontsize=45, labelpad=10)
	plt.subplot(312)
	plt.ylabel('$L_{max} (10^{43}erg s^{-1})$', fontsize=40, labelpad=5)
	#plt.savefig('lbolt2_bf.pdf')

main()
