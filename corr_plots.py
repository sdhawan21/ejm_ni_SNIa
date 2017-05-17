"""
Plots figure 1 for Ni masses from the stored lbol values and makes a pdf in the plot_rel directory



fontsize and manager (families etc.) made publication worthy

other than that, seems vanilla plotting


"""
from matplotlib.pyplot import *
from matplotlib import font_manager
from matplotlib.ticker import MultipleLocator
from string import upper
from scipy.stats import pearsonr

import numpy as np
rcParams['axes.linewidth']=2.5
rcParams['xtick.major.size']=8
rcParams['xtick.minor.size']=4
rcParams['ytick.major.size']=6
rcParams['ytick.minor.size']=3
rcParams['ytick.major.pad']=13
rcParams['xtick.major.pad']=13
sizeOfFont = 35			
fontProperties = {'family':'serif','serif':['Times New Roman'],
    'weight' : 'normal', 'size' : sizeOfFont}
ticks_font = font_manager.FontProperties(family='Times New Roman', style='normal',
    size=sizeOfFont, weight='normal', stretch='normal')
fig=figure(figsize=(12, 18))					#figsize and fontproperties
mni=np.loadtxt('mni_lcbol.txt', dtype='string')
#tv=np.loadtxt('tab_val.tex', dtype='string', delimiter='&', usecols=(0, 3, 2, -1))
tv=np.loadtxt('tables/u_flags.txt', dtype='string', skiprows=1)
tv=tv[tv[:,3]=='UBVRIJH']
filt=['y', 'j', 'h']
c=['yD', 'g.', 'rs']
sl=[311, 312, 310]
pt='/home/sdhawan/tests_paper/csp_sn/sec_max_files/'
pt1='/home/sdhawan/bol_ni_ej/'
e=[i[0][0:-1] for i in tv]
#tv[:,0]=e
for k in range(3):
	sp=np.loadtxt(pt+filt[k]+'_sec_max_csp.dat', dtype='string')
	#sp=np.loadtxt(pt1+'m55_tex/m55_'+filt[k]+'.tex', delimiter='&', dtype='string')
	#sp[:,0]=np.array([mk[0][0:-1] for mk in sp])
	n=[float(i[1]) for i in tv if i[0] in sp[:,0]]
	en=[float(i[2]) for i in tv if i[0] in sp[:,0]]
	t=[float(sp[sp[:,0]==i[0]][0][1]) for i in tv if i[0] in sp[:,0]]
	et=[float(sp[sp[:,0]==i[0]][0][2]) for i in tv if i[0] in sp[:,0]]
	s1=subplot(sl[k])
	xlim(10, 40)
	s1.tick_params('both', length=15, width=2)
	s1.minorticks_on()
	s1.xaxis.set_major_locator(MultipleLocator(10))
	s1.tick_params('both', length=7, which='minor')
	errorbar(t, n, xerr=et, yerr=en, fmt=c[k], ms=15, elinewidth=2.5)
	frame=gca()
	print pearsonr(n, t), len(n)
	d=frame.axes.get_yticklabels()
	d[0].set_fontsize(0)
	d[-1].set_fontsize(0)
	for h in d:
		if h != d[0] and h != d[-1]:
			h.set_fontproperties(ticks_font)
	if k !=2:
		c1=frame.axes.get_xticklabels()
		for m in c1:
			m.set_fontsize(0)
	else:
		c1=frame.axes.get_xticklabels()
		for m in c1:
			m.set_fontproperties(ticks_font)
	t=np.array(t);vs=np.vstack([t, np.ones(len(t))]).T; a=np.linalg.lstsq(vs, n)[0]
	plot(t, a[0]*np.array(t)+a[1], 'k:')
	annotate(upper(filt[k]), xy=(0.1, 0.8), xycoords='axes fraction', fontsize=40, weight='bold', family='times new roman' )
xlabel('$t_{2}$', labelpad=15, fontsize=40, family='times new roman')
subplot(312)
ylabel('$L_{Bol} (*1e43 erg/s)$', labelpad=15, fontsize=30, family='times new roman')
subplots_adjust(hspace=0)
savefig('plot_rel/err_bf_slbol.pdf')
