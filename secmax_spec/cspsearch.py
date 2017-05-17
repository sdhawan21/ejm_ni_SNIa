"""
i-band second maximum line search: CSP data

(should not be restrictive to CSP data. Any release with spectra should be read in)


"""
from glob import glob
from pack import sn91bg #also works for non 91bg


import matplotlib.pyplot as plt
import numpy as np
import sys
#define alias for defspec class

ds=sn91bg.defspec()
def rdhead(infile):
	t=open(infile, 'r')
	ls=[]
	for row in t:
		ls.append(row.split())
	return ls[:6]
class specwrite:
	pt='/home/sdhawan/'
	ptdir='neb_spec/CSP_spectra_DR1/'
	def write_spec(self):
		
		
	
		sset=[]
	
		indir=sorted(glob(self.pt+self.ptdir+'*.dat'))
		for i in indir:
			head=rdhead(i)
			ep=float(head[5][1])
			if ep > 15 and ep < 30:
				wv, fl=np.loadtxt(i, unpack=True)
				if max(wv) > 9000:
					sset.append([head[0][1], i, ep])
		np.savetxt('files/spectra.txt', sset, fmt='%s')			
		print len(sset)
def main():
	#in_range_spec=np.loadtxt('files/spectra.txt')
	specdir= sorted(glob(specwrite.pt+specwrite.ptdir+'*.dat'))		
	sn=sys.argv[1]
	inspec_dir=ds.pullspec(specdir, sn)
	
	specwrite().write_spec()
	
	spec1=int(sys.argv[2][0])
	spec2=int(sys.argv[2][1:])
	epochs=np.array([ds.get_phase(i) for i in inspec_dir])
	
	wv, fl=np.loadtxt(inspec_dir[spec1], unpack=True)
	
	wv1, fl1 = np.loadtxt(inspec_dir[spec2], unpack=True)
	print epochs[spec1], epochs[spec2]
	plt.plot(wv, fl,  linewidth=2, label="Epoch: "+str(epochs[spec1]))
	plt.plot(wv1, fl1, alpha=0.2, label="Epoch: "+str(epochs[spec2]))
	
	plt.legend(loc=0)
	plt.xlabel('$\lambda (\AA)$')
	plt.ylabel('Flux')	
	plt.title(sn)
	plt.show()
if len(sys.argv) == 3:	
	main()
else:
	print "Usage: python "+sys.argv[1]+ '<SN> <first/second spectra>'
