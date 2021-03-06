pro mklcbol, infile,$                ;input file (see sn2005cf_lcbolinput.dat for format)
             pbinfo=pbinfo,$         ;file with passband information
             bands=bands,$           ;select these bands by default e.g. bands='UBVRI' or bands=['U','B','V','R','I']
;             refband=refband,$       ;select this reference band by default
             interpmeth=interpmeth,$ ;interpolation method [l]inear lsquadrati[c] q[u]adratic [s]pline
             dtinterp=dtinterp,$     ;ensure there are points in range [t-dtinterp,t] and [t,t+dtinterp] for interpolation
             batch=batch,$           ;set /batch for batch (non-interactive) mode
             fout=fout               ;user-defined output file (overrides default filename)

;  
; Generate (pseudo)-bolometric light curves
;
; TODO:
;
; - implement 2nd & 3rd-order poly fit + error
;
; - check pbinfo.dat; add vega-weighted effective wavelength? add more
;   filters (especially NIR e.g. Kprime_MKO, Ks_MKO etc.)? add
;   SN-template-weighted lambda_eff?
;
; - user input for interpolation (change method, delete/undelete
;   points, remove entire filter etc.); implement dtinterp=
;
; - do not allow filter to have its blue edge < lambda_eff of
;   previous filter (i.e. overlap > 50%); warn user about (large) gaps?
;
; - add buttons with typical filter choices e.g. UBVRI, SwiftUV, JHKs,
;   All, etc.
;
; - add time label to integrated filter plots; add inset or separate
;   window showing lcbol?
;
; - always assume UBVRI=Bessell (optpb= keyword? -- see MLCS2k2),
;   JHKs=MKO (or 2MASS?)
;
; - allow AB magnitudes?
;

;
; constants
;
EPS_TIME = 1d-2 ;use actual measurement over interpolation if abs(time-t)<EPS_TIME

;
; defaults
;
if not keyword_set(pbinfo) then PBINFO='~/idl/lcbol/pbinfo.dat' ;file with passband info (effective wavelength, EW)
if not keyword_set(interpmeth) then interpmeth='c'
if not keyword_set(dtinterp) then dtinterp=3.0



;
; read in input file
;
rd_lcbol_data, infile, hdr, lcdata
print,'### generating pseudo-bolometric LC for '+hdr.name



;
; get filter info, sort by increasing effective wavelength
;
readcol,PBINFO,pbname,lambda_eff,ew,zpt,f='a,d,d,d',comment='#',/silent
struct = {name:'',shortname:'',lambda_eff:0.0,ew:0.0,zpt:0.0}
filt = replicate(struct,hdr.nfilt)
idx = 0
newlcdata = lcdata
for i=0,hdr.nfilt-1 do begin
   rr = where(pbname eq lcdata[i].filt,nrr)
   if (nrr eq 0) then begin
      print,' WARNING - filter '+lcdata[i].filt+' is not part of '+PBINFO
   endif else begin
      newlcdata[idx] = lcdata[i]
      filt[idx].name = lcdata[i].filt
      case filt[idx].name of
         'uvw2_Swift': filt[idx].shortname='uvw2' 
         'uvm2_Swift': filt[idx].shortname='uvm2' 
         'uvw1_Swift': filt[idx].shortname='uvw1' 
         'uu_Swift':   filt[idx].shortname='u'
         'bb_Swift':   filt[idx].shortname='b'
         'vv_Swift':   filt[idx].shortname='v'
         'U_Bessell':  filt[idx].shortname='U'
         'B_Bessell':  filt[idx].shortname='B'
         'V_Bessell':  filt[idx].shortname='V'
         'R_Bessell':  filt[idx].shortname='R'
         'I_Bessell':  filt[idx].shortname='I'
         'u_prime':    filt[idx].shortname='u'''
         'g_prime':    filt[idx].shortname='g'''
         'r_prime':    filt[idx].shortname='r'''
         'i_prime':    filt[idx].shortname='i'''
         'z_prime':    filt[idx].shortname='z'''
         'J_MKO':     filt[idx].shortname='J'
         'H_MKO':     filt[idx].shortname='H'
         'K_MKO':     filt[idx].shortname='Ks' ;CHECK! K or Ks?
         'Kprime_MKO':filt[idx].shortname='Kp' 
         'J_2MASS':   filt[idx].shortname='J'
         'H_2MASS':   filt[idx].shortname='H'
         'Ks_2MASS':  filt[idx].shortname='Ks'
         else: filt[idx].shortname=filt[idx].name
      endcase
      filt[idx].lambda_eff = lambda_eff[rr]
      filt[idx].ew = ew[rr]
      filt[idx].zpt = zpt[rr]
      idx++
   endelse
endfor
if (idx lt 3) then message,'Need at least 2 filters!'
hdr.nfilt = idx
lcdata = newlcdata[0:idx-1]
filt = filt[0:idx-1]

rrsort = sort(filt.lambda_eff)
lcdata = lcdata[rrsort]
filt = filt[rrsort]



;
; filter selection
;
idxselect = lonarr(hdr.nfilt)
;rrselect=[4,6,8,10,12] & idxselect[rrselect]=1 & nselect=5 ;TEST
if keyword_set(bands) then begin
   if (size(bands,/dimensions) eq 0) then begin
      case strlowcase(bands) of
         'all': bands=['U_Bessell','B_Bessell','V_Bessell','R_Bessell','I_Bessell','J_2MASS','H_2MASS','Ks_2MASS']
         'opt': bands=['U','B','V','R','I']+'_Bessell'
         'opt_nou': bands=['B','V','R','I']+'_Bessell'
         'nir': bands=['J','H','Ks']+'_2MASS'
         else: begin
            nb = strlen(bands)
            dum = strarr(nb)
            for i=0,nb-1 do dum[i]=strmid(bands,i,1)
            bands = dum
         end
      endcase
   endif
   for i=0,n_elements(bands)-1 do begin
      rr = where(filt.name eq bands[i],nrr)
      if (nrr eq 1) then idxselect[rr]=1 else begin
         print,' WARNING - No entry for filter '+bands[i]+' in '+infile
         rr = where(filt.shortname eq bands[i],nrr)
         if (nrr eq 1) then idxselect[rr]=1 else begin
            print,' WARNING - No entry for filter '+bands[i]+' in '+infile
         endelse
      endelse
   endfor
   rrselect = where(idxselect eq 1,nselect)
endif
if keyword_set(batch) then begin
   print,strtrim(string(nselect,f='(i)'),2)+$
         ' selected filters: '+strjoin(filt[rrselect].name,',')
   goto,skipok
endif



;
; plot available light curves, user selection of filters to combine
;
WUVOPT = 3000.  ;wavelength boundary between UV/optical (A)
WOPTIR = 10000. ;wavelength boundary between optical/IR (A)
col_uv  = 'purple'
col_opt = 'green'
col_ir  = 'red'

;common x-axis range to all plots
tmin =  9d9
tmax = -9d9
for i=0,hdr.nfilt-1 do begin
   dum1 = min(*lcdata[i].time)
   dum2 = max(*lcdata[i].time)
   if (dum1 lt tmin) then tmin=dum1
   if (dum2 gt tmax) then tmax=dum2
endfor
;print,'tmin,tmax= ',tmin,tmax
dt = tmax-tmin
xrlc = [tmin,tmax]+[-1,1]*dt*.05
if (xrlc[0] gt 1e4) then begin
   milmjd = (long(xrlc[0])/1000)*1000
   xtitdefault='MJD - '+strtrim(string(milmjd,f='(i)'),2)
endif else begin
   milmjd = 0
   xtitdefault = 'Time'
endelse
xrlc = xrlc-milmjd

;set up plot grid
if (hdr.nfilt eq 2) then begin
   nx = 2
   ny = 1
endif else if (hdr.nfilt gt 2 and hdr.nfilt le 4) then begin
   nx = 2
   ny = 2
endif else if (hdr.nfilt gt 4 and hdr.nfilt le 6) then begin
   nx = 3
   ny = 2
endif else if (hdr.nfilt gt 6 and hdr.nfilt le 9) then begin
   nx = 3
   ny = 3
endif else if (hdr.nfilt gt 9 and hdr.nfilt le 12) then begin
   nx = 4
   ny = 3
endif else if (hdr.nfilt gt 12 and hdr.nfilt le 16) then begin
   nx = 4
   ny = 4
endif else if (hdr.nfilt gt 16 and hdr.nfilt le 20) then begin
   nx = 5
   ny = 4
endif else if (hdr.nfilt gt 20 and hdr.nfilt le 25) then begin
   nx = 5
   ny = 5
endif else if (hdr.nfilt gt 25 and hdr.nfilt le 30) then begin
   nx = 6
   ny = 5
endif else if (hdr.nfilt gt 30 and hdr.nfilt le 36) then begin
   nx = 6
   ny = 6
endif else message,'Cannot plot this many filters!'

;all sizes in cm
xsize = 6.0 ;x-size of individual LC plot
ysize = 4.0 ;y-size of individual LC plot
xspace = .6 ;x-space between LC plots
yspace = .6 ;y-space between LC plots
ysizefilt = 3.0 ;y-size of filter plot
yspacefilt = 1.5 ;vertical space between LC plots and filter plot

okwidth = 2.0 ;width of OK button
okheight = 1.0
yspaceok = 0.5 ;vertical space between filter plot and OK button

ubvriwidth = 2.0 ;width of UBVRI button
ubvriheight = 1.0
yspaceubvri = 0.5 ;vertical space between filter plot and UBVRI button

bvrioff = 0.3 ;horizontal offset from previous button
bvriwidth = 2.0 ;width of BVRI button
bvriheight = 1.0
yspacebvri = 0.5 ;vertical space between filter plot and BVRI button

leftmargin  = 1.5
rightmargin = 0.5
bottommargin = 1.0
topmargin = 0.5
xwindowsize = leftmargin + nx*xsize + (nx-1)*xspace + rightmargin
ywindowsize = bottommargin + ny*ysize + (ny-1)*yspace + yspacefilt + ysizefilt + yspaceok + okheight + topmargin

;cm -> normal coords conversion factors
xcm2norm = 1.0/xwindowsize
ycm2norm = 1.0/ywindowsize

;window size in pixels
oinfo = obj_new('IDLsysMonitorInfo')
res = oinfo->getresolutions() ;screen x,y-resolution in cm/pix
obj_destroy,oinfo
xwindowsizepix = xwindowsize/res[0]
ywindowsizepix = ywindowsize/res[1]
window,0,title='Generate pseudo-bolometric light curves',xsize=xwindowsizepix,ysize=ywindowsizepix

;plot filter transmission curves
x0filt = leftmargin * xcm2norm
x1filt = (leftmargin + nx*xsize + (nx-1)*xspace) * xcm2norm
y0filt = (bottommargin + ny*ysize + (ny-1)*yspace + yspacefilt) * ycm2norm
y1filt = y0filt + ysizefilt * ycm2norm
posfilt = [x0filt,y0filt,x1filt,y1filt]

xmin = min(filt.lambda_eff-filt.ew/2.)
xmax = max(filt.lambda_eff+filt.ew/2.)
dx = xmax-xmin
xrfilt = [xmin,xmax]+[-1,1]*dx*.05
yrfilt = [0,1.19]

;idxselect = lonarr(hdr.nfilt)
;;rrselect=[4,6,8,10,12] & idxselect[rrselect]=1 & nselect=5 ;TEST
;if keyword_set(bands) then begin
;   if (size(bands,/dimensions) eq 0) then begin
;      nb = strlen(bands)
;      dum = strarr(nb)
;      for i=0,nb-1 do dum[i]=strmid(bands,i,1)
;      bands = dum
;   endif
;   for i=0,n_elements(bands)-1 do begin
;      rr = where(filt.shortname eq bands[i],nrr)
;      if (nrr gt 0) then idxselect[rr]=1
;   endfor
;   rrselect = where(idxselect eq 1,nselect)
;endif

filtplot:
plot,xrfilt,yrfilt,xr=xrfilt,/xs,yr=yrfilt,/ys,xtit='Wavelength (A)',ytit='Transmission',/nodata,$
     xtickformat='(i)',pos=posfilt
ylab = 1.05
for i=0,hdr.nfilt-1 do begin
   wfiltblue = filt[i].lambda_eff-filt[i].ew/2.
   wfiltred  = filt[i].lambda_eff+filt[i].ew/2.
   colfilt = 'white'
   thickfilt = 1
   if (idxselect[i] eq 1) then begin
      if (filt[i].lambda_eff lt WUVOPT) then begin
         colfilt = col_uv
      endif else if (filt[i].lambda_eff gt WOPTIR) then begin
         colfilt = col_ir
      endif else begin
         colfilt = col_opt
      endelse
      thickfilt = 2
   endif
   plots,replicate(wfiltblue,2),[0,1],col=cgcolor(colfilt),thick=thickfilt
   plots,replicate(wfiltred,2),[0,1],col=cgcolor(colfilt),thick=thickfilt
   plots,[wfiltblue,wfiltred],[1,1],col=cgcolor(colfilt),thick=thickfilt
;   if (ylab lt 1.) then ylab=1.05 else ylab=.88
   xyouts,filt[i].lambda_eff,ylab,/data,alignment=.5,filt[i].shortname,col=cgcolor(colfilt)
endfor

;plot light curves
x0lc = x0filt
x1lc = x1filt
y0lc = bottommargin * ycm2norm
y1lc = (bottommargin + ny*ysize + (ny-1)*yspace) * ycm2norm
xspacenorm = xspace * xcm2norm
yspacenorm = yspace * ycm2norm
poslc = getplotpos(nx,ny,xmin=x0lc,ymin=y0lc,xmax=x1lc,ymax=y1lc,vspace=yspacenorm,hspace=xspacenorm)

lcplot:
plotsym,0,1,/fill
for i=0,hdr.nfilt-1 do begin
   
   if (filt[i].lambda_eff lt WUVOPT) then begin
      col = col_uv
   endif else if (filt[i].lambda_eff gt WOPTIR) then begin
      col = col_ir
   endif else begin
      col = col_opt
   endelse
   
   ymin = min(*lcdata[i].mag-*lcdata[i].magerr)
   ymax = max(*lcdata[i].mag+*lcdata[i].magerr)
   dy = ymax-ymin
   yrlc = [ymax,ymin]+[1,-1]*dy*.05
   
   thepos = [poslc.x0[i],poslc.y0[i],poslc.x1[i],poslc.y1[i]]
   if (abs(thepos[0]-x0lc) lt 1e-5) then ytit='Mag' else ytit=''
   if (abs(thepos[1]-y0lc) lt 1e-5) then xtit=xtitdefault else xtit=''
   
   if (idxselect[i] eq 1) then begin
      xpoly = [thepos[0],thepos[2],thepos[2],thepos[0]]
      ypoly = [thepos[1],thepos[1],thepos[3],thepos[3]]
      polyfill,xpoly,ypoly,/normal,col=cgcolor('charcoal')
   endif
   plot,xrlc,yrlc,xr=xrlc,/xs,yr=yrlc,/ys,/nodata,ytickformat='(i)',$
        xtit=xtit,ytit=ytit,pos=thepos,/noerase
   oploterror,*lcdata[i].time-milmjd,*lcdata[i].mag,*lcdata[i].magerr,$
              col=cgcolor(col),errcol=cgcolor(col),psym=8
   
   dxx = thepos[2]-thepos[0]
   dyy = thepos[3]-thepos[1]
   xlab = thepos[2]-dxx*.04
   ylab = thepos[3]-dyy*.1
   xyouts,xlab,ylab,/normal,alignment=1.,filt[i].name
   
endfor

;OK button
x0ok = (xwindowsize - rightmargin - okwidth) * xcm2norm
x1ok = (xwindowsize - rightmargin) * xcm2norm
y0ok = (ywindowsize - topmargin - okheight) * ycm2norm
y1ok = (ywindowsize - topmargin) * ycm2norm
plots,[x0ok,x1ok,x1ok,x0ok,x0ok],[y0ok,y0ok,y1ok,y1ok,y0ok],/normal,thick=2
xoklab = 0.5*(x0ok+x1ok)
yoklab = y0ok + (y1ok-y0ok)*.25
xyouts,xoklab,yoklab,/normal,'OK',alignment=0.5,charsize=2.5,charthick=2

;UBVRI button
x0ubvri = leftmargin * xcm2norm
x1ubvri = (leftmargin + ubvriwidth) * xcm2norm
y0ubvri = (ywindowsize - topmargin - ubvriheight) * ycm2norm
y1ubvri = (ywindowsize - topmargin) * ycm2norm
plots,[x0ubvri,x1ubvri,x1ubvri,x0ubvri,x0ubvri],[y0ubvri,y0ubvri,y1ubvri,y1ubvri,y0ubvri],/normal,thick=2
xubvrilab = 0.5*(x0ubvri+x1ubvri)
yubvrilab = y0ubvri + (y1ubvri-y0ubvri)*.25
xyouts,xubvrilab,yubvrilab,/normal,'UBVRI',alignment=0.5,charsize=2.25,charthick=1.5

;BVRI button
x0bvri = (leftmargin + ubvriwidth + bvrioff) * xcm2norm
x1bvri = (leftmargin + ubvriwidth + bvrioff + bvriwidth) * xcm2norm
y0bvri = (ywindowsize - topmargin - bvriheight) * ycm2norm
y1bvri = (ywindowsize - topmargin) * ycm2norm
plots,[x0bvri,x1bvri,x1bvri,x0bvri,x0bvri],[y0bvri,y0bvri,y1bvri,y1bvri,y0bvri],/normal,thick=2
xbvrilab = 0.5*(x0bvri+x1bvri)
ybvrilab = y0bvri + (y1bvri-y0bvri)*.25
xyouts,xbvrilab,ybvrilab,/normal,'BVRI',alignment=0.5,charsize=2.25,charthick=1.5

;user selection with mouse
idxplot=-1 & ok=0 & ubvri=0 & bvri=0
;ok=1 & goto,skipok ;TEST
print,'Click on light curves to select/deselect filters; click OK button when done'
repeat begin
   cursor,xc,yc,/down,/normal
   if (xc ge x0ok and xc le x1ok and yc ge y0ok and yc le y1ok) then begin
      polyfill,[x0ok,x1ok,x1ok,x0ok],[y0ok,y0ok,y1ok,y1ok],/normal,col=cgcolor('charcoal')
      plots,[x0ok,x1ok,x1ok,x0ok,x0ok],[y0ok,y0ok,y1ok,y1ok,y0ok],/normal,thick=2
      xyouts,xoklab,yoklab,/normal,'OK',alignment=0.5,charsize=2.5,charthick=2
      ok = 1
   endif else if (xc ge x0ubvri and xc le x1ubvri and yc ge y0ubvri and yc le y1ubvri) then begin
      polyfill,[x0ubvri,x1ubvri,x1ubvri,x0ubvri],[y0ubvri,y0ubvri,y1ubvri,y1ubvri],/normal,col=cgcolor('charcoal')
      plots,[x0ubvri,x1ubvri,x1ubvri,x0ubvri,x0ubvri],[y0ubvri,y0ubvri,y1ubvri,y1ubvri,y0ubvri],/normal,thick=2
      xyouts,xubvrilab,yubvrilab,/normal,'UBVRI',alignment=0.5,charsize=2.25,charthick=1.5
      thebands = ['U','B','V','R','I']
      idxselect = lonarr(hdr.nfilt)
      for i=0,n_elements(thebands)-1 do begin
         rr = where(filt.shortname eq thebands[i],nrr)
         if (nrr gt 0) then idxselect[rr]=1
      endfor
      rrselect = where(idxselect eq 1,nselect)
      ubvri = 1
      goto,filtplot
   endif else if (xc ge x0bvri and xc le x1bvri and yc ge y0bvri and yc le y1bvri) then begin
      polyfill,[x0bvri,x1bvri,x1bvri,x0bvri],[y0bvri,y0bvri,y1bvri,y1bvri],/normal,col=cgcolor('charcoal')
      plots,[x0bvri,x1bvri,x1bvri,x0bvri,x0bvri],[y0bvri,y0bvri,y1bvri,y1bvri,y0bvri],/normal,thick=2
      xyouts,xbvrilab,ybvrilab,/normal,'BVRI',alignment=0.5,charsize=2.25,charthick=1.5
      thebands = ['B','V','R','I']
      idxselect = lonarr(hdr.nfilt)
      for i=0,n_elements(thebands)-1 do begin
         rr = where(filt.shortname eq thebands[i],nrr)
         if (nrr gt 0) then idxselect[rr]=1
      endfor
      rrselect = where(idxselect eq 1,nselect)
      bvri = 1
      goto,filtplot
   endif else begin
      idxx=-1 & idxy=-1
      for ii=0,hdr.nfilt-1 do $
         if (xc ge poslc.x0[ii] and xc le poslc.x1[ii]) and $
            (yc ge poslc.y0[ii] and yc le poslc.y1[ii]) then idxplot=ii
   endelse
endrep until (idxplot ge 0 and idxplot le hdr.nfilt-1 or ok eq 1 or ubvri eq 1 or bvri eq 1)
if (ok eq 1) then begin
   rrselect = where(idxselect eq 1,nselect)
   if (nselect lt 2) then begin
      print,'Need to select at least 2 filters'
      goto,filtplot
   endif else begin
      print,strtrim(string(nselect,f='(i)'),2)+$
            ' selected filters: '+strjoin(filt[rrselect].name,',')
      repeat begin
         print,'Is this OK? [y/n] or [q]uit (default=y)'
         c = get_kbrd(1)
         c = strlowcase(c)
         if ((byte(c))[0] EQ 10) then c = 'y'
         print, c
      endrep until (c eq 'y') or (c eq 'n')  or (c eq 'q')
      if (c eq 'q') then begin
         print,'Exiting program'
         goto,fin
      endif else if (c eq 'n') then begin
         goto,filtplot
      endif
   endelse
endif else if (idxselect[idxplot] eq 0) then begin
   print,' INFO - selected filter '+lcdata[idxplot].filt
   idxselect[idxplot] = 1
   goto,filtplot
endif else begin
   print,' INFO - deselected filter '+lcdata[idxplot].filt
   idxselect[idxplot] = 0
   goto,filtplot
endelse


skipok:
;
; get reference filter for interpolation
;

;find largest tmin and smallest tmax
tmin = -9d9
tmax =  9d9
tarr = -9d9
for i=0,nselect-1 do begin
   idx = rrselect[i]
   tt = *lcdata[idx].time
   dum1 = min(tt)
   dum2 = max(tt)
   if (dum1 gt tmin) then tmin=dum1
   if (dum2 lt tmax) then tmax=dum2
   tarr = [tarr,tt]
endfor
tarr = tarr[1:n_elements(tarr)-1]
rr = where(tarr ge tmin and tarr le tmax)
tt = tarr[rr]
time_interp = tt[uniq(tt,sort(tt))]
nt = n_elements(time_interp)
interpmag = fltarr(nselect,nt)
interpmagerr = fltarr(nselect,nt)
;print,'tmin,tmax,minmax(time_interp)= ',tmin,tmax,minmax(time_interp)

;### DON'T USE REFERENCE BAND - USE ALL POINTS IN RANGE [TMIN,TMAX]
;;pick reference filter (one with most points in range [tmin,tmax]; or
;;one specified with refband= keyword)
;numpts = 0
;if keyword_set(refband) then reffilt=refband else begin
;   for i=0,nselect-1 do begin
;      idx = rrselect[i]
;      rr = where(*lcdata[idx].time ge tmin and *lcdata[idx].time le tmax,nrr)
;      if (nrr gt numpts) then begin
;         reffilt = filt[idx].name
;         numpts = nrr
;      endif
;   endfor
;endelse
;pickreffilt:
;if not keyword_set(batch) then begin
;   print,'Reference filter is: '+reffilt
;   repeat begin
;      print,'Is this OK? [y/n] (default=y)'
;      c = get_kbrd(1)
;      c = strlowcase(c)
;      if ((byte(c))[0] eq 10) then c = 'y'
;      print, c
;   endrep until (c eq 'y') or (c eq 'n')
;   if (c eq 'n') then begin
;      print,'Enter new reference filter; choices are:'
;      for i=0,nselect-1 do begin
;         idx = rrselect[i]
;         print,'('+strtrim(string(i+1,f='(i)'),2)+') '+filt[idx].name
;      endfor
;      repeat begin
;         c = get_kbrd(1)
;         filtnum = long(c)
;      endrep until (filtnum ge 1 and filtnum le nselect)
;      idx = rrselect[filtnum-1]
;      reffilt = filt[idx].name
;      goto,pickreffilt
;   endif
;endif
;
;
;
;;
;; interpolate all other lightcurves on time axis of reference filter
;;
;rr = where(filt.name eq reffilt)
;time_reffilt = *lcdata[rr].time
;rr = where(time_reffilt ge tmin and time_reffilt le tmax,nrr)
;time_interp = time_reffilt[rr]
;
;;ensure tmin,tmax are part of time_interp array
;if (abs(time_interp[0]-tmin) gt 1e-5) then time_interp = [tmin,time_interp]
;if (abs(time_interp[nrr-1]-tmax) gt 1e-5) then time_interp = [time_interp,tmax]
;nt = n_elements(time_interp)
;interpmag = fltarr(nselect,nt)

;interpolate all filters on time_interp array
if not keyword_set(batch) then begin
   wdelete,0
   dt = tmax-tmin
   xrinterp = [tmin,tmax]+[-1,1]*dt*.1 - milmjd
   plotsym,0,1,/fill
endif

;skip filter
skipfilt = lonarr(nselect)
print, rrselect, nselect
for i=0,nselect-1 do begin

   idx = rrselect[i]

   ;plot original and interpolated light curves
   xx = *lcdata[idx].time
   yy = *lcdata[idx].mag
   yyerr = *lcdata[idx].magerr
   if not keyword_set(batch) then begin
      rr = where(xx-milmjd ge xrinterp[0] and xx-milmjd le xrinterp[1])
      ymin = min(yy[rr]-yyerr[rr])
      ymax = max(yy[rr]+yyerr[rr])
      dy = ymax-ymin
      yrinterp = [ymax,ymin]+[1,-1]*dy*.1
      newinterpmeth:
      plot,xrinterp,yrinterp,/nodata,xr=xrinterp,/xs,yr=yrinterp,/ys,xtit=xtitdefault,ytit='Mag'
      oploterror,xx-milmjd,yy,yyerr,psym=8
   endif

   ;interpolation method
   if interpmeth eq 'l' then begin
      for ii=0,nt-1 do begin
         ;don't interpolate if we hit an actual point
         dum = min(abs(xx-time_interp[ii]),rrmin)
         if (dum lt EPS_TIME) then begin
            interpmag[i,ii] = yy[rrmin]
            interpmagerr[i,ii] = yyerr[rrmin]
         endif else begin
            ;bracket points
            rri = max(where(xx le time_interp[ii]))
            rrs = min(where(xx ge time_interp[ii]))
            xlin = [xx[rri],xx[rrs]]
            ylin = [yy[rri],yy[rrs]]
            ylinerr = [yyerr[rri],yyerr[rrs]]
            a = linfit(xlin,ylin,measure_errors=ylinerr,sigma=sigma,covar=covar)
            interpmag[i,ii] = a[0] + a[1]*time_interp[ii]
            interpmagerr[i,ii] = sqrt( (time_interp[ii]*sigma[1])^2 + sigma[0]^2 + $
                                       2*time_interp[ii]*covar[0,1] )
         endelse
      endfor
   endif else begin
      lsquadratic=0 & quadratic=0 & spline=0 
      case interpmeth of
         'c': lsquadratic=1
         'u': quadratic=1
         's': spline=1
         else:
      endcase
      yyinterp = interpol(yy,xx,time_interp,$
                          spline=keyword_set(spline),$
                          lsquadratic=keyword_set(lsquadratic),$
                          quadratic=keyword_set(quadratic))
      interpmag[i,*] = yyinterp
   endelse

   if not keyword_set(batch) then begin
      oploterror,time_interp-milmjd,interpmag[i,*],interpmagerr[i,*],$
                 psym=8,col=cgcolor('green'),errcol=cgcolor('green'),/nohat
      
      dxx = xrinterp[1]-xrinterp[0]
      dyy = yrinterp[0]-yrinterp[1]
      xlab = xrinterp[1]-dxx*.04
      ylab = yrinterp[1]+dyy*.1
      dylab = dyy*.05
      xyouts,xlab,ylab,/data,alignment=1.,filt[idx].name,charsize=2.
      xyouts,xlab,ylab+dylab,/data,alignment=1.,'Original data',charsize=1.5
      xyouts,xlab,ylab+2*dylab,/data,alignment=1.,'Interpolated data',col=cgcolor('green'),charsize=1.5
      
      repeat begin
         print,'Is this OK? [y/n] (default=y)'
         c = get_kbrd(1)
         c = strlowcase(c)
         if ((byte(c))[0] eq 10) then c = 'y'
         print, c
      endrep until (c eq 'y') or (c eq 'n')

      if (c eq 'n') then begin
         ;TODO - USER SELECTS DIFFERENT INTERPOLATION METHODS,
         ;       DELETES/UNDELETES POINTS ETC.
         repeat begin
            print,'Change [i]nterpolation method; [s]kip filter; or [q]uit? (default=i)'
            c = get_kbrd(1)
            c = strlowcase(c)
            if ((byte(c))[0] EQ 10) then c = 'i'
            print, c
         endrep until (c eq 'i') or (c eq 's') or (c eq 'q')
         if (c eq 'q') then begin
            print,'Exiting program'
            goto,fin
         endif else if (c eq 's') then begin
            print,'Ok, will ignore filter: '+filt[idx].name
            skipfilt[i] = 1
         endif else if (c eq 'i') then begin
            repeat begin
               print,'Select new interpolation method (current='+interpmeth+'): [l]inear lsquadrati[c] q[u]adratic [s]pline'
               c = get_kbrd(1)
               c = strlowcase(c)
               print, c
            endrep until (c eq 'l') or (c eq 'c') or (c eq 'u') or (c eq 's')
            interpmeth = c
            goto,newinterpmeth
         endif
      endif
   endif

endfor

;check for skipped filters
rr = where(skipfilt eq 0,nrr)
if (nrr eq 0) then begin
   message,'No filters left!'
endif else begin
   lcdata = lcdata[rr]
   interpmag = interpmag[rr,*]
   rrselect = rrselect[rr]
   nselect = nrr
endelse



;
; convert de-redenned magnitudes to fluxes 
;
interpflux = dblarr(nselect,nt)
interpfluxerr = interpflux ;includes extinction error
for i=0,nselect-1 do begin
   idx = rrselect[i]
   AlAv_host = al_av(filt[idx].lambda_eff,r_v=hdr.rvhost,rverr=hdr.rvhosterr)
   AlAv_MW = al_av(filt[idx].lambda_eff,r_v=hdr.rvmw,rverr=hdr.rvmwerr)
   
   Al_host = AlAv_host[0] * hdr.avhost
   print, 'The RV  and al host are', Al_host
   Al_MW   = AlAv_MW[0] * hdr.avmw
   Al_tot = Al_host[0] + Al_MW[0]
   interpflux[i,*] = 10^(-0.4*(interpmag[i,*]-Al_tot[0]-filt[idx].zpt))
   ;CHECK - PROPAGATE EXTINCTION ERROR
   if hdr.avhost gt 0.0 then $
      Al_host_err = Al_host[0] * sqrt( (AlAv_host[1]/AlAv_host[0])^2 + (hdr.avhosterr/hdr.avhost)^2 ) else $
      Al_host_err = 0.0
   if hdr.avmw gt 0.0 then $
      Al_MW_err = Al_MW[0] * sqrt( (AlAv_MW[1]/AlAv_MW[0])^2 + (hdr.avmwerr/hdr.avmw)^2 ) else $
      Al_MW_err = 0.0
   Al_tot_err = sqrt( Al_host_err^2 + Al_MW_err^2 )
   interpfluxerr[i,*] = interpflux[i,*] * (0.4*alog(10)*Al_tot_err/Al_tot)
endfor



;
; integrate fluxes (trapezoidal), dealing with overlaps and gaps
;

;;### Valenti style - WARNING: INPROPER TREATMENT OF GAPS AND OVERLAPS 
;;### TODO: ERROR CALCULATION
;leftedge  = interpflux[0,*] * filt[rrselect[0]].ew / 2.
;rightedge = interpflux[nselect-1,*] * filt[rrselect[nselect-1]].ew / 2.
;flux_int = dblarr(nt)
;for i=0,nselect-2 do begin
;   dist = filt[rrselect[i+1]].lambda_eff - filt[rrselect[i]].lambda_eff
;   fluxmean = 0.5 * (interpflux[i,*] + interpflux[i+1,*])
;   flux_int += fluxmean * dist
;endfor
;flux_int += leftedge + rightedge
;
;;plot fluxes at each time?
;if not keyword_set(batch) then begin
;   xmin = min(filt[rrselect].lambda_eff-filt[rrselect].ew/2.)
;   xmax = max(filt[rrselect].lambda_eff+filt[rrselect].ew/2.)
;   dx = xmax-xmin
;   xrfilt = [xmin,xmax]+[-1,1]*dx*.05
;   dxx = xrfilt[1]-xrfilt[0]
;   for i=0,nt-1 do begin
;      ymax = max(interpflux[*,i])
;      yrfilt = [0,ymax*1.05]
;      dyy = yrfilt[1]-yrfilt[0]
;      plot,xrfilt,yrfilt,xr=xrfilt,/xs,yr=yrfilt,/ys,xtit='Wavelength (A)',ytit='Flux',/nodata,$
;           xtickformat='(i)'
;      xlab = xrfilt[1]-dxx*.04
;      ylab = yrfilt[1]-dyy*.1
;      dylab = dyy*.05
;      xyouts,xlab,ylab,/data,alignment=1.,'Flux in each filter',charsize=1.5
;      xyouts,xlab,ylab-dylab,/data,alignment=1.,'Integrated flux',col=cgcolor('red'),charsize=1.5
;      
;      ;flux level in each filter
;      for ii=0,nselect-1 do begin
;         idx = rrselect[ii]
;         x0 = filt[idx].lambda_eff-filt[idx].ew/2.
;         x1 = filt[idx].lambda_eff+filt[idx].ew/2.
;         yy = interpflux[ii,i]
;         plots,[x0,x0,x1,x1],[0,yy,yy,0],thick=4
;         xyouts,filt[idx].lambda_eff,yy-dyy*.05,/data,alignment=.5,filt[idx].shortname,charsize=2.,charthick=2.
;      endfor
;
;      ;flux levels for integration
;      x0 = filt[rrselect[0]].lambda_eff-filt[rrselect[0]].ew/2. ;left edge
;      x1 = filt[rrselect[0]].lambda_eff
;      yyl = interpflux[0,i]
;      plots,[x0,x0,x1],[0,yyl,yyl],col=cgcolor('red'),thick=2
;
;      x0 = filt[rrselect[nselect-1]].lambda_eff ;right edge
;      x1 = filt[rrselect[nselect-1]].lambda_eff+filt[rrselect[nselect-1]].ew/2.
;      yyr = interpflux[nselect-1,i]
;      plots,[x0,x1,x1],[yyr,yyr,0],col=cgcolor('red'),thick=2
;
;      fluxmean = dblarr(nselect-1)
;      for ii=0,nselect-2 do fluxmean[ii] = 0.5 * (interpflux[ii,i] + interpflux[ii+1,i])
;      for ii=0,nselect-2 do begin
;         x0 = filt[rrselect[ii]].lambda_eff 
;         x1 = filt[rrselect[ii+1]].lambda_eff
;         if (ii eq 0) then begin
;            y0 = yyl
;            y1 = fluxmean[ii]
;            y2 = fluxmean[ii+1]
;            plots,[x0,x0,x1,x1],[y0,y1,y1,y2],col=cgcolor('red'),thick=2
;         endif else if (ii eq nselect-2) then begin
;            y0 = fluxmean[ii]
;            y1 = yyr
;            plots,[x0,x1,x1],[y0,y0,y1],col=cgcolor('red'),thick=2
;         endif else begin
;            y0 = fluxmean[ii]
;            y1 = fluxmean[ii+1]
;            plots,[x0,x1,x1],[y0,y0,y1],col=cgcolor('red'),thick=2
;         endelse
;      endfor
;   ;   print,'Hit any key to continue, or [q]uit'
;   ;   zzz = get_kbrd(1)
;   ;   if (zzz eq 'q') then i=nt-1
;      i = nt-1
;   endfor
;endif


;### correct treatment of gaps and overlaps
flux_int = dblarr(nt)
flux_int_err = flux_int
idxlap = 0 ;set =1 if current filter overlapped with previous one
for i=0,nselect-1 do begin
   idx = rrselect[i]
   if (i gt 0 and idxlap eq 1) then wblue=wred else wblue=filt[idx].lambda_eff-filt[idx].ew/2.
   if (i lt nselect-1) then begin ;all but last filter
      wred = filt[idx].lambda_eff+filt[idx].ew/2.
      idxnext = rrselect[i+1]
      wbluenext = filt[idxnext].lambda_eff-filt[idxnext].ew/2.
      if (wred le wbluenext) then begin ;isolated filter => gap between this and next filter
         flux_int += (wred-wblue) * interpflux[i,*] ;FILTER
         flux_int += (wbluenext-wred) * (interpflux[i,*]+interpflux[i+1,*])/2. ;GAP - take mean flux
         flux_int_err += (wred-wblue) * interpfluxerr[i,*]
         flux_int_err += (wbluenext-wred) * sqrt(interpfluxerr[i,*]^2+interpfluxerr[i+1,*]^2)/2.
         idxlap = 0
      endif else begin ;overlap with next filter
         flux_int += (wbluenext-wblue) * interpflux[i,*] ;FILTER
         flux_int += (wred-wbluenext) * (interpflux[i,*]+interpflux[i+1,*])/2. ;OVERLAP - take mean flux
         flux_int_err += (wbluenext-wblue) * interpfluxerr[i,*]
         flux_int_err += (wred-wbluenext) * sqrt(interpfluxerr[i,*]^2+interpfluxerr[i+1,*]^2)/2.
         idxlap = 1
      endelse
   endif else begin ;last filter - no overlap possible with next filter
      flux_int += (wred-wblue) * interpflux[i,*]
      flux_int_err += (wred-wblue) * interpfluxerr[i,*]
   endelse
endfor

;plot fluxes at each time?
if not keyword_set(batch) then begin
   xmin = min(filt[rrselect].lambda_eff-filt[rrselect].ew/2.)
   xmax = max(filt[rrselect].lambda_eff+filt[rrselect].ew/2.)
   dx = xmax-xmin
   xrfilt = [xmin,xmax]+[-1,1]*dx*.05
   dxx = xrfilt[1]-xrfilt[0]
   for i=0,nt-1 do begin
      ymax = max(interpflux[*,i])
      yrfilt = [0,ymax*1.05]
      dyy = yrfilt[1]-yrfilt[0]
      plot,xrfilt,yrfilt,xr=xrfilt,/xs,yr=yrfilt,/ys,xtit='Wavelength (A)',ytit='Flux',/nodata,$
           xtickformat='(i)'
      xlab = xrfilt[1]-dxx*.04
      ylab = yrfilt[1]-dyy*.1
      dylab = dyy*.05
      xyouts,xlab,ylab,/data,alignment=1.,'Flux in each filter',charsize=1.5
      xyouts,xlab,ylab-dylab,/data,alignment=1.,'Integrated flux',col=cgcolor('red'),charsize=1.5
      
      ;flux level in each filter
      for ii=0,nselect-1 do begin
         idx = rrselect[ii]
         x0 = filt[idx].lambda_eff-filt[idx].ew/2.
         x1 = filt[idx].lambda_eff+filt[idx].ew/2.
         yy = interpflux[ii,i]
         plots,[x0,x0,x1,x1],[0,yy,yy,0],thick=4
         xyouts,filt[idx].lambda_eff,yy-dyy*.05,/data,alignment=.5,filt[idx].shortname,charsize=2.,charthick=2.
      endfor

      ;flux levels for integration
      idxlap = 0                ;set =1 if current filter overlapped with previous one
      y1prev = 0.
      for ii=0,nselect-1 do begin
         idx = rrselect[ii]
         if (ii gt 0 and idxlap eq 1) then wblue=wred else wblue=filt[idx].lambda_eff-filt[idx].ew/2.
         wred = filt[idx].lambda_eff+filt[idx].ew/2.
         if (ii lt nselect-1) then begin ;all but last filter
            idxnext = rrselect[ii+1]
            wbluenext = filt[idxnext].lambda_eff-filt[idxnext].ew/2.
            if (wred le wbluenext) then begin             ;isolated filter => gap between this and next filter
               y0 = interpflux[ii,i]                      ;FILTER
               y1 = (interpflux[ii,i]+interpflux[ii+1,i])/2. ;GAP - take mean flux
               plots,[wblue,wblue,wred,wred,wbluenext],[y1prev,y0,y0,y1,y1],col=cgcolor('red'),thick=2
               idxlap = 0
               y1prev = y1
            endif else begin                              ;overlap with next filter
               y0 = interpflux[ii,i]                      ;FILTER
               y1 = (interpflux[ii,i]+interpflux[ii+1,i])/2. ;OVERLAP - take mean flux
               plots,[wblue,wblue,wbluenext,wbluenext,wred],[y1prev,y0,y0,y1,y1],col=cgcolor('red'),thick=2
               idxlap = 1
               y1prev = y1
            endelse
         endif else begin       ;last filter - no overlap possible with next filter
            y0 = interpflux[ii,i]
            plots,[wblue,wblue,wred,wred],[y1prev,y0,y0,0.],col=cgcolor('red'),thick=2
         endelse
      endfor
      print,'Hit any key to continue, or [q]uit'
      zzz = get_kbrd(1)
      if (zzz eq 'q') then i=nt-1
   endfor
endif



;
; compute final luminosity = flux_int * 4piR^2, R=10^((dmod+5)/5) pc
; Rerr=R*ln(10)*dmoderr/5 - CHECK !
; TODO - ERROR CALCULATION
; Lerr = sqrt( 2*(Rerr/R)^2 + (Fint_err/Fint)^2 )
;
dist_cm = 3.085677d18 * 10^((hdr.dmod+5.)/5.)
dist_cm_err = dist_cm * alog(10) * hdr.dmoderr/5.
lum_int = 4*!pi*dist_cm^2 * flux_int
lum_int_err = lum_int * sqrt( 2*(dist_cm_err/dist_cm)^2 + (flux_int_err/flux_int)^2 )
print, flux_int


;
; output file
;
if not keyword_set(fout) then fout=hdr.name+'_lcbol_'+strjoin(filt[rrselect].shortname)+'.dat'
openw,uout,fout,/get_lun
printf,uout,'#generated on '+systime()+' using mklcbol.pro'
printf,uout,'#'
printf,uout,'#INFILE   '+strtrim(strmid(infile,strpos(infile,'/',/reverse_search)+1),2)
printf,uout,'#NAME     '+strtrim(hdr.name,2)
printf,uout,'#AV_HOST  '+strtrim(string(hdr.avhost,f='(f6.3)'),2)+' +/- '+strtrim(string(hdr.avhosterr,f='(f6.3)'),2)
printf,uout,'#RV_HOST  '+strtrim(string(hdr.rvhost,f='(f6.3)'),2)+' +/- '+strtrim(string(hdr.rvhosterr,f='(f6.3)'),2)
printf,uout,'#AV_MW    '+strtrim(string(hdr.avmw,f='(f6.3)'),2)+' +/- '+strtrim(string(hdr.avmwerr,f='(f6.3)'),2)
printf,uout,'#RV_MW    '+strtrim(string(hdr.rvmw,f='(f6.3)'),2)+' +/- '+strtrim(string(hdr.rvmwerr,f='(f6.3)'),2)
printf,uout,'#DIST_MOD '+strtrim(string(hdr.dmod,f='(f6.3)'),2)+' +/- '+strtrim(string(hdr.dmoderr,f='(f6.3)'),2)
printf,uout,'#NFILT    '+strtrim(string(nselect,f='(i2)'),2)+' ('+strjoin(filt[rrselect].name,',')+')'
printf,uout,'#'
printf,uout,'#time[d]','lbol[erg/s]','lbolerr[erg/s]',f='(a-11,2(2x,a-15))'
for i=0,nt-1 do printf,uout,time_interp[i],lum_int[i],lum_int_err[i],f='(f10.3,2(2x,E15.8))'
free_lun,uout
print,'Created file '+fout

fin:
!p.multi=0
end
