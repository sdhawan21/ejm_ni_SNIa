import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d

class read_lightcurve:
	
	def __init__(self):
		self.path = '/home/sdhawan/workspaces/cfair2/'
		
	def load_file(self, filename='cfair2.dat'):
		ff = np.loadtxt('/home/sdhawan/workspaces/cfair2/cfair2.dat', dtype='string', skiprows=31)
		return ff
	def read_sn(self, sn):
		ff = self.load_file()
		
		return ff[ff[:,0] == sn]
	
	def read_filter(self, sn, filt):
	
		sn1 = self.read_sn(sn)
		sn_lc = sn1[sn1[:,3] == filt]
		vs= np.vstack([sn_lc[:,5].astype('float32'), sn_lc[:,-2].astype('float32'), sn_lc[:, -1].astype('float32')]).T
		
		return vs[vs[:,0].argsort()]
	

class spline_fit:
	
	def __init__(self):
		self.tmax = np.loadtxt('/home/sdhawan/workspaces/cfair2/tmax_dm15.dat', dtype='string')
	
	def fit_band(self, sn, band, pl='No'):
		"""
		Shift the filtered light curve to the B-maximum (using SNPy spline fits)
		
		Use scipy.interpolate to spline fit the light curve in the filter
		"""
		lc = read_lightcurve().read_filter(sn, band)
		
		tm = float(self.tmax[self.tmax[:,0] == sn][0][1])
		lc[:,0] -=tm 
		
		
		spl = interp1d(lc[:,0], lc[:,1], kind='cubic')
		
		ll = np.linspace(lc[:,0].min(), lc[:,0].max(), 200)
		
		gl = spl(ll)
		
		gl_max = gl[ll < 10]
		ll_max = ll[ll<10]
		
		if pl=='Yes':
			plt.plot(ll, gl)
			plt.plot(lc[:,0], lc[:,1], 'rs')
			plt.show()
		return min(gl), ll[gl == min(gl)], min(gl_max), ll_max[gl_max==min(gl_max)] 
	def fit_t2_sne(self, sn, band, pl='No'):
		"""
		Shift the filtered light curve to the B-maximum (using SNPy spline fits)
		
		Use scipy.interpolate to spline fit the light curve in the filter
		"""
		lc = read_lightcurve().read_filter(sn, band)
		
		tm = float(self.tmax[self.tmax[:,0] == sn][0][1])
		lc[:,0] -=tm 
		
		
		spl = interp1d(lc[:,0], lc[:,1], kind='cubic')
		
		ll = np.linspace(lc[:,0].min(), lc[:,0].max(), 200)
		
		gl = spl(ll)
		
		gl_max = gl[ll > 5]
		ll_max = ll[ll > 5]
		
		if pl=='Yes':
			plt.plot(ll, gl)
			plt.plot(lc[:,0], lc[:,1], 'rs')
			plt.show()
		return  min(gl_max), ll_max[gl_max==min(gl_max)][0] 
