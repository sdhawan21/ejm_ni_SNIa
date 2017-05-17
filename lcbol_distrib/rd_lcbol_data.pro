pro rd_lcbol_data, infile, hdr, lcdata

;
; Read input file for mklcbol.pro (see sn2005cf_lcbolinput.dat for format)
;

openr,uin,infile,/get_lun

;read in header info
okhdr=0 & line=''
while (okhdr eq 0) do begin
   readf,uin,line
   linearr = strsplit(line,' ',/extract,count=narr)
   case linearr[0] of
      '#NAME': name=linearr[1]
      '#AV_HOST': begin
         avhost = float(linearr[1])
         if (narr gt 3) then avhosterr=float(linearr[3]) else avhosterr=0.0
      end
      '#RV_HOST': begin
         rvhost = float(linearr[1])
         if (narr gt 3) then rvhosterr=float(linearr[3]) else rvhosterr=0.0
      end
      '#AV_MW': begin
         avmw = float(linearr[1])
         if (narr gt 3) then avmwerr=float(linearr[3]) else avmwerr=0.0
      end
      '#RV_MW': begin
         rvmw = float(linearr[1])
         if (narr gt 3) then rvmwerr=float(linearr[3]) else rvmwerr=0.0
      end
      '#DIST_MOD': begin
         dmod = float(linearr[1])
         if (narr gt 3) then dmoderr=float(linearr[3]) else dmoderr=0.0
      end
      '#NFILT': begin
         nfilt = long(linearr[1])
         okhdr = 1
      end
      else:
   endcase
endwhile

;header structure
hdr = {name:name,avhost:avhost,avhosterr:avhosterr,rvhost:rvhost,rvhosterr:rvhosterr,$
       avmw:avmw,avmwerr:avmwerr,rvmw:rvmw,rvmwerr:rvmwerr,dmod:dmod,dmoderr:dmoderr,$
       nfilt:nfilt}

;data
lcstruct = {filt:'',time:ptr_new(),mag:ptr_new(),magerr:ptr_new()}
lcdata = replicate(lcstruct,nfilt)

for i=0,nfilt-1 do begin
   while (strpos(line,'#FILTER') lt 0) do readf,uin,line
   linearr = strsplit(line,' ',/extract)
   lcdata[i].filt = linearr[1]
   print,'[ INFO  ] reading filter '+linearr[1]
   nmeas = float(linearr[3])
   time = fltarr(nmeas)
   mag = time
   magerr = time
   for ii=0,nmeas-1 do begin
      readf,uin,line
      linearr = strsplit(line,' ',/extract)
      time[ii] = float(linearr[0])
      mag[ii] = float(linearr[1])
      magerr[ii] = float(linearr[2])
   endfor
   lcdata[i].time = ptr_new(1)
   *lcdata[i].time = time
   lcdata[i].mag = ptr_new(1)
   *lcdata[i].mag = mag
   lcdata[i].magerr = ptr_new(1)
   *lcdata[i].magerr = magerr 
endfor

free_lun,uin

end