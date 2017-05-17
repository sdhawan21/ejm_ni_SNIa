"""
Looking into decline rate correlations for fast decliners

Usage: python declcorrs.py line decline rate

Prints: 
pearsonr coefficient for
	a. line and decline rate
	b. line and decline rate for low-luminosity objects (as given by a certain decline rate range.)
	
1: s_BV
2: delta m_ 15 

Choose wisely!

"""

import numpy as np
import matplotlib.pyplot as plt
import sys

from scipy.stats import pearsonr

qtt=sys.argv[3]
def readtables():
	intab1=np.loadtxt('../csptables/table_ew_max.tex', dtype='string', delimiter='&')
	intab2=np.loadtxt('../csptables/table_sne.tex', dtype='string', delimiter='&')
	return intab1, intab2

def select_vals(ind, qtt):
	it1, it2 = readtables()
	
	stab=np.loadtxt('../../burns14_ebv.tex', delimiter='&', dtype='string')
	if qtt == 'vel':
		it1=np.loadtxt('../csptables/table_vel_max.tex', delimiter='&', dtype='string')	
		ran = [3,9]
	elif qtt== 'ew':
		ran = [4,8]
	
	dm15=[i[-5][4:9] for i in it2 if i[0]+ ' ' in it1[:,0] and i[0] in stab[:,0]]
	
	ew=[it1[it1[:,0]==i[0]+' '][0][ind][ran[0]:ran[1]] for i in it2 if i[0]+ ' ' in it1[:,0] and i[0] in stab[:,0]] 
	
	sbv=[stab[stab[:,0]==i[0]][0][3][1:5] for i in it2 if i[0]+ ' ' in it1[:,0] and i[0] in stab[:,0]]
	#print i[0]+' ' in it1[:,0]
	
	nm=[it1[it1[:,0]==i[0]+' '][0][0] for i in it2 if i[0]+ ' ' in it1[:,0] and i[0] in stab[:,0]] 
	
	
	
	
	
	return np.array(dm15), np.array(ew), np.array(sbv), np.array(nm)

if qtt== 'ew':
	pws=['cahk', 'si4130', 'mgII', 'feII', 'SIIW', 'SiII5972', 'SiII6355', 'cair']
elif qtt == 'vel':
	pws=['cahk', 'si4130', 's5449', 's5622', 'si5972', 'si6355', 'cair', 'v20']
	
def main():
	
	

	line=sys.argv[1]
	
	
	# 1 for Sbv and 2 for dm15
	
	decl=int(sys.argv[2])
	
	ind=pws.index(line)
	dm15, ew, sbv,nm=select_vals(ind+1, qtt)
	
	darr=[]; ewarr=[]; sarr=[]; nmarr=[]
	#print nm[ew==min(ew)], sbv[ew==min(ew)], ew
	
	#return 0
	
	for i  in range(len(dm15)):
		try:
			a=float(dm15[i])
			b=float(ew[i])
			c=float(sbv[i])
			darr.append(a)
			ewarr.append(b)
			sarr.append(c)
			nmarr.append(nm[i])
		except:
			i
	sarr=np.array(sarr); darr=np.array(darr); ewarr=np.array(ewarr); nmarr=np.array(nmarr)
	if decl == 1:
		decarr=sarr
		cond=(sarr < 0.6)
		xlab= '$s_{BV}$'
	elif decl == 2:
		decarr=darr 
		cond = (darr > 1.5)
		xlab = '$\Delta m_{15}$'
	print pearsonr(decarr, ewarr), pearsonr(ewarr[cond], decarr[cond])#, len(darr)
	
	np.savetxt(qtt+'_'+line+'.txt', np.vstack([nmarr[cond], ewarr[cond], decarr[cond]]).T, '%s')
	plt.plot(decarr, ewarr, 'r^')
	plt.plot(decarr[cond], ewarr[cond], 'bo')
	plt.xlabel(xlab)
	plt.ylabel(qtt+'\t'+line)
	plt.show()
if len(sys.argv) == 4:
	main()
else:
	print 'Usage: python', sys.argv[0], ' <which line> <which param> with possible line measurements', pws
