"""
H0 from NIR peak magnitude of SN Ia

formula is in the summary in notes/ directory

Models:
	-> DDC (Blondin et al. 2015)
	-> PDD (Dessart et al. 2014)
	-> SCH (Blondin et al. in prep)

ZP sources:
	-> Kattner et al. 2012
	-> Folatelli et al. 2010
equations:
	ZP = 25 - log10(H0)/.2 - Mpeak 
	H0 = 10	^ (.2 * (Mmax - ZP + 25))
Usage: python h0_est.py <filter> <model> 
"""


from pack import dist

import numpy as np
import sys


class model:
	"""
	Extract the model peak magnitude from the files given by Stephane
	"""

	#filter set array
	farr =['Y', 'J', 'H']

	def __init__(self, filename):
		self.filename = filename
		
	
	def vals(self, filt, mod):
		
		infile = np.loadtxt(self.filename, dtype='string')
		sset = np.array([i for i in infile if mod in i[0]])
		f_val = sset[sset[:,1] == filt] 
		return f_val[:,3].astype('float32')
		
	

	def mag_vals(self, a1):
		arr = a1[a1> -900]
		return np.mean(arr), np.std(arr)/np.sqrt(len(arr))

class obs:
	"""
	use the mean peak and error from CSP papers to create a zero point
	"""
	rn = np.random.normal
	def __init__(self, h0, mpeak):
		self.h0 = h0
		self.mpeak = mpeak
	
	
	def zp(self):
		#derive zeropoint from H0 and mean peak
		h_cons = self.h0
		m = self.mpeak
		
		ar= [25-np.log10(h_cons)/0.2 + self.rn(m[0], m[1]) for k in range(100000)]
		
		return np.mean(ar), np.std(ar)
		
		
		

def main():
	#define command line inputs
	filt = sys.argv[1]	#YJH
	mod = sys.argv[2]	#DDC,PDD,SCH
	
	
	h0 = 72			#H0 used by folatelli et al./Kattner et al.
	

	#which file to use for the input model (note: PDD and SCH have the same file)
	files = np.loadtxt('file.lis', dtype='string')
	infile = files[files[:,0] == mod][0][1]
	
	#file for the mpeak and error values
	mfile = np.loadtxt('kattner.dat', dtype='string')
	mval = mfile[mfile[:,0]==filt][0]
	
	marr = [float(mval[1]), float(mval[2])]
	
	#open the h0 output file
	fout = open('h0.lis', 'a')
	
	#load model class
	mod_cls = model(infile)
	magarr = mod_cls.mag_vals(mod_cls.vals(filt, mod))
	
	print "The mean and error from the model ", mod, "is:", magarr[0], magarr[1]
	
	#load observations class
	obs_cls = obs(h0, marr)
	
	#zero point and error
	z, ez = obs_cls.zp()
	print "The zero point for filter ", filt, " is:", round(z, 3), round(ez,3)

	# propagate a 0.03 mag uncertainty in the photometric zero point
	#use the H0 monte carlo function from pack
	h0=dist.h0_mc(magarr, [z, np.sqrt(ez**2 + 0.03**2)], 1000)
	
	print h0
	
	fout.write('For model '+mod+'and filter '+filt+'the H0 is '+str(h0[0])+'\t'+str(h0[1])+'\n')
	
	fout.close()
if __name__=="__main__":	
	main()

