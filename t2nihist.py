import numpy as np
import mag2fl as mf
import matplotlib.pyplot as plt

from string import upper

rn=np.random.normal
filt=['y', 'j']
c=['y', 'g']
snlr=np.loadtxt('sn_samp_lr.tex', dtype='string', delimiter='&')[:,0]
for k in range(2):
	y=np.loadtxt('mod_tab'+upper(filt[k])+'-exp.tex', delimiter='&', dtype='string')
	t0=[]
	nm=[]
	print y[0][5]
	for i in y:
		try:
			#print i[5][1:5]
			print i[0]
			if 'SN'+i[0] not in snlr:
				t0.append(float(i[5][2:7]))
				nm.append(i[0])
		except:
			i
	t0=np.array(t0)
	print t0
	#nn=mf.corr_bf().trans(t0, filt[k])
	nn=0.042*np.array(t0)-0.056
	plt.subplot(210+k)
	arr=zip(nm, nn)
	np.savetxt('out_files/nihist_'+filt[k]+'.txt', arr,fmt='%s')





#plotting functions, currently commented out

"""
	
	plt.annotate(upper(filt[k]), xy=(0.1, 0.8), xycoords='axes fraction')
	plt.hist(nn, color=c[k], alpha=0.3, bins=np.arange(0.1, 0.9, 0.05))
plt.subplot(210)
plt.xlabel('$M_{Ni}$')
plt.subplot(211)
plt.ylabel('$N_{SN}$')
plt.savefig('plot_rel/nihist_rel.pdf')
"""
