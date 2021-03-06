"""
	Module contains all functions required for 91bg-like analysis
class for spectra	
	--obtain name, phase
	--get spectra for a given SN
	--plot spectra from an input array

class for bollc
"""
import numpy as np
import matplotlib.pyplot as plt
import os


from glob import glob
from itertools import *
class defspec:
	#infile=np.loadtxt('/home/sdhawan/bol_ni_ej/fast_decl/all91bg.txt', dtype='string')
	def get_head(self, spec):
		"""
		Extract the header from the spectrum file
		"""
		ls=[]
		infile=open(spec, 'r')
		for row in infile:
			ls.append(row.split())
		return ls[:6]
	def get_name(self, spec):
		"""
		Get SN name from header
		"""
		head=self.get_head(spec)
		return head[0][1]
	def get_phase(self, spec):
		"""
		Get information about spectrum epoch from header
		"""
		head=self.get_head(spec)
		return float(head[5][1])
	def get_z(self, spec):
		"""
		Get redshift info from header
		"""
		head=self.get_head(spec)
		return float(head[2][1])
	def pullspec(self, specdir, name):
		"""
		Using the name as input, pull out all spectra of the CSP
		"""
		sset=[]
		for i in specdir:
			nm=self.get_name(i)
			if nm==name:
				sset.append(i)
		return sset
	def plotspec(self, arr1, ran, fac):
		"""
		Plot a set of spectra from an array
		-- fine tunes the factor by which the labels should be spaced 
		"""
		arr=arr1[ran[0]:ran[1]]
		s=cycle(['s', 'o', '+', '^', 'D'])
		f=cycle(['r', 'g', 'b', 'k', 'm', 'y'])
		o=0
		for i in arr:
			
			wv, fl=np.loadtxt(i, unpack=True)
			plt.plot(wv/(1+self.get_z(i)), o*5+(fl/max(fl)), next(f)+':') #next(f)+next(s))
			plt.annotate(self.get_name(i)+'  '+str(self.get_phase(i)),xy=(0.85, 0.95-(o/fac)), xycoords='axes fraction')
			o+=.2
			print o
			plt.xlabel('$\lambda (\AA)$ ')
			plt.ylabel('Normalised flux + offset')
			plt.show()
			#plt.savefig('91bg_spec_opt.png')
class bollc:
	def get_bol_head(self, lc):
		"""
		Extract the header from the lc file
		"""
		ls=[]
		infile=open(lc, 'r')
		for row in infile:
			ls.append(row.split())
		return ls[:10]
	def get_bol_name(self, lc):
		head=self.get_bol_head(lc)
		return head[3][1]
"""
class cfaspec:
	
	pt='/home/sdhawan/neb_spec/cfaspec_snIa/'
	indir=glob(pt+'sn*')
	
	mjd=np.loadtxt(pt+'cfasnIa_mjdspec.dat', dtype='string')
	bmax=np.loadtxt(pt+'cfasnIa_param.dat', dtype='string')
	def getcfaspec(self, sn, num):
		
		os.chdir(self.pt+sn)
		dirsn=glob('*.flm')
		spec=dirsn[num]
		mjdspec=self.mjd[self.mjd[:,0]== spec][0][1]
		mjdspec=float(mjdspec)

		wv, fl, flerr=np.loadtxt(spec, unpack=True)
		tbmax=self.bmax[self.bmax[:,0] == sn[2:]][0][2]
		tbmax=float(tbmax)
		print mjdspec-tbmax
		plt.plot(wv, fl)
		plt.show()
		
		return mjdspec-tbmax
"""		
		
	
