"""
Create the files for the complete sample (non-low red) 


"""
import numpy as np
import mag2fl as mf
import matplotlib.pyplot as plt

from string import upper

#shorthand for function
rn=np.random.normal

#filters and colours if plotting
filt=['y', 'j']
c=['y', 'g']

#best fit coefficients 
co_arr=[[[0.045, 0.005], [-0.150, 0.140]], [[0.042, 0.005], [-0.056, 0.122]]]

#load the file with lr SN for the names
snlr=np.loadtxt('sn_samp_lr.tex', dtype='string', delimiter='&')[:,0]


#loop over the two filters
for k in range(2):
	#load the t2 values 
	y=np.loadtxt('mod_tab'+upper(filt[k])+'-exp.tex', delimiter='&', dtype='string')
	t0=[]
	nm=[]
	et0=[]
	print y[0][5]
	#distribute the t2's into the appropriate arrays
	for i in y:
		try:
			#print i[5][1:5]
			print i[5][12:16]
			if 'SN'+i[0] not in snlr:
				t0.append(float(i[5][2:7]))
				nm.append(i[0])
				et0.append(float(i[5][12:16]))
		except:
			i
	#convert to arrays
	t0=np.array(t0)
	et0=np.array(et0)
	print t0, et0
	
	
	nn=np.zeros([len(t0), 2])
	
	for l in range(len(t0)):
	
		#combined coefficients. With higher errors (for conservative estimates)
		coeff=[[0.0415, 0.005], [-0.073, 0.140]]#co_arr[k]
		#array of realisations for lmax
		
		
		narr=[(rn(coeff[0][0], coeff[0][1])*rn(t0[l], et0[l])+rn(coeff[1][0], coeff[1][1])) for j in range(1000)]
		nn[l][0]=round(np.mean(narr), 2)
		nn[l][1]=round(np.std(narr), 2)
	plt.subplot(210+k)
	arr=np.vstack([nm, nn[:,0], nn[:,1]]).T#zip(nm, nn)
	np.savetxt('out_files/new_lbolhist_'+filt[k]+'.txt', arr,fmt='%s')





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
