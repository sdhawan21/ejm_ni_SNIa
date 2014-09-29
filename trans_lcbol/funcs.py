import numpy as np
import sys 

pt='/Users/lapguest/all_paper/files_snpy/'
tmax=np.loadtxt(pt+'tmax_dm15.dat', dtype='string')
bselect=sys.argv[1]
pbin=np.loadtxt("csp_info.dat", dtype='string')
class flux_conv:   #conversion of light curves to filter fluxes, no propagation of distances yet. (do so after the trapezoidal) 
	def spt_conv(self, mag, zp):
                return pow(10, -0.4*(mag-zp)) 
        def all_time(self, pharr, filt):
                arr=[]
                rr=np.array([i[0] for i in pbin[:,0]])
                zp=float(pbin[rr==filt][0][3])
                for i in pharr:
                        fl=self.spt_conv(i[1], zp)
                        arr.append(fl)
                return np.array(arr)

                
class dist:
        def mu2cm(self, mu):
                mpc2=3.08e24**2
                ff=4*np.pi*pow(10, ((mu-25)/5.0))
                return ff*mpc2
class interp:
#Valenti style integration (trapezoidal)
	def fl_int(self,f,m, filt):
           fl_int=0
           lamb=pbin[:,1].astype('float32')
           filt=flux_conv().all_time(f,filt )
           dist=lamb[m+1]-lamb[m]
           fluxmean=0.5*(filt)
           #fl_int+=fluxmean*dist
           return fluxmean*dist

                        
