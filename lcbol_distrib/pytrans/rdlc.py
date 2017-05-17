import numpy as np

h='/home/sdhawan/pap_files/CSP_Photometry_DR2/'
tl='opt+nir_photo.dat'
class rd_bol_data:
	def rdlc(self, sn):
		f=open(h+sn+tl, 'r')
		f1=np.loadtxt(h+sn+tl, skiprows=5)
		ls=[]
		for row in f:
			ls.append(row.split())
		filt=[]
		for rr in ls[4]:
			if rr !='+/-' and  rr != 'MJD' and rr != '#':
				filt.append(rr)
	#	ind=ls[4].index(band)
		lc={}
		print ls[4], filt
		for fl in filt:			
			ind=ls[4].index(fl)
			lc['MJD'+fl]=f1[:,0][f1[:,ind]<90]
			lc[fl]=f1[:,ind-1][f1[:,ind]<90]
			lc['e_'+fl]=f1[:,ind][f1[:,ind]<90]		
		return lc
print rd_bol_data().rdlc('SN2007on')







