import numpy as np
import mag2fl as mf
import matplotlib.pyplot as plt

from string import upper


filt=['y', 'j']
c=['y', 'g']
for k in range(2):
	y=np.loadtxt('../csp_sn/'+filt[k]+'_pap.tex', delimiter='&', dtype='string')
	t0=[]
	nm=[]
	for i in y:
		try:
			t0.append(float(i[7][0:6]))
			nm.append(i[0])
		except:
			i
	t0=np.array(t0)
	nn=mf.corr_bf().trans(t0, filt[k])
	plt.subplot(210+k)
	arr=zip(nm, nn)
	np.savetxt('plot_rel/nihist'+filt[k]+'.txt', arr,fmt='%s')
	plt.annotate(upper(filt[k]), xy=(0.1, 0.8), xycoords='axes fraction')
	plt.hist(nn, color=c[k], alpha=0.3, bins=np.arange(0.1, 0.9, 0.05))
plt.subplot(210)
plt.xlabel('$M_{Ni}$')
plt.subplot(211)
plt.ylabel('$N_{SN}$')
plt.savefig('plot_rel/nihist_rel.pdf')