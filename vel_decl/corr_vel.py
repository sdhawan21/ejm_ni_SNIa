import numpy as np
import mag2fl as mf
import pickle as pc
import matplotlib.pyplot as plt
bsn=np.loadtxt('/home/sdhawan/cats_astroquery/blondin_si_params.dat', dtype='string', skiprows=1, usecols=(1, 2, 3, 4))
from scipy.stats import pearsonr
#print mf.spl_fit().lt_dec('2005eq', 'B', 'cfa')
nm=[i[0][:-1] for i in bsn]
print bsn[bsn[:,-1].astype('float32') > -9000]
vsi=[]
dec=[]

excl_list =['2002cx', '2002es', '2005hk', '2007if', '2009dc']

for i in nm:
	if i not in excl_list:
		try:
			w=pc.load(open('cfa_lc/'+i+'_lc.txt', "rb"))	
			d=mf.spl_fit().lt_dec(i, 'B', 'cfa')
			dec.append(d[0])
			v=float(bsn[nm.index(i)][3])
			vsi.append(v)
		except:
			i
vsi=np.array(vsi); dec=np.array(dec)
print vsi, dec
a=(dec<0.03) & (dec>0.000) #& (vsi<-9000)
#fout=open('notes.txt', 'a')
#fout.write("Pearson coefficients \t"+str(pearsonr(dec[a], vsi[a]))+'\n')
print len(vsi[a]), pearsonr(dec[a], vsi[a])
plt.plot(dec[a], vsi[a], 'r+')
plt.xlabel('$B-band$ decline')
plt.ylabel('$v_{si}$')
plt.show()



