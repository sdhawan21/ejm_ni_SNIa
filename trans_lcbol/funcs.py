import numpy as np
import sys 

pt='/Users/lapguest/all_paper/files_snpy/'
tmax=np.loadtxt(pt+'tmax_dm15.dat', dtype='string')
bselect=sys.argv[1]
class flux_conv:   #conversion of light curves to filter fluxes, no propagation of distances yet. (do so after the trapezoidal) 
	def spt_conv(self, mag, zp):
                return pow(10, -0.4*(mag-zp)) 
        def all_time(self, pharr):
                arr=[]
                for i in pharr:
                        fl=self.spt_conv(i[1], zp)
                        arr.append(fl)
                return np.array(arr)

                

class interp:
#Valenti style integration (trapezoidal)
	def fl_int(self,flarr):
           for i in range(nfilt):
                   dist=lamb[i+1]-lamb[i]
                   fluxmean=0.5*(flarr)
                   fl_int+=fluxmean*dist


