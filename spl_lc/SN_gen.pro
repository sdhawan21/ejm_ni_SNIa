PRO SN_gen

filesfind=file_search('/home/sdhawan/neb_spec/CSP_spectra_DR1/SN04*.dat')


file_ls=[]

ls4=[]
ls5=[]
ls6=[]
ls7=[]
h=size(filesfind)
For i = 0,20 do begin 
   readcol, filesfind(i), wv, flux;, flux_err
   subset=where(wv gt 5800 and wv lt 6350)

  ; line_norm, wv(subset), flux(subset), ynorm, norm

   wv1=wv(subset)
   ;flux_err1=flux_err(subset)
   ;b=flux_err1/norm
   ynorm=flux(subset)
   aa=mpfitpeak(wv1, ynorm, output_guess)
   peak=output_guess(1)


   e=peak-275
   g=peak+275
   ls=[]
   ls1=[]
   ls2=[]
   ls3=[]
   
   for j=0, 9 do begin  
      subset1=where(wv1 gt e and wv1 lt g) 
      aa=mpfitpeak(wv1(subset1), ynorm(subset1), output_guess)
      ls=[ls, chisq1/dof1]
      ls1=[ls1, output_guess(1)]
      e=e+10
      g=g-10
      ls2=[ls2, e]
      ls3=[ls3, g]
   
      
   endfor 
   
   c=min(ls)
   subset2=where(ls eq c)

   ls4=[ls4, ls(subset2)]
   ls5=[ls5, ls1(subset2)]
   ls6=[ls6, ls2(subset2)]
   ls7=[ls7, ls3(subset2)]

   a=ls2(subset2)
   b=ls3(subset2)
   sub3=where(wv1 gt a(0) and wv1 lt b(0))
   wv2=wv1(sub3)
   ynorm1=ynorm(sub3)
   b1=b(sub3)


   aa1=mpfitpeak(wv2, ynorm1, output_guess)
   plot, wv1, ynorm
   oplot, wv2, aa1
   
   file_ls=[file_ls, filesfind(i)]
   
   peak_ls=[]
   g=a(0)
   n=b(0)
   for i=0,10 do begin
   sub4=where(wv1 gt g(0) and wv1 lt h(0))
   aa2=mpfitpeak(wv1(sub4), ynorm(sub4), output_guess)
   peak_ls=[peak_ls, output_guess(1)]
   g=g-1
   h=h+1
   endfor
error_ls=[]

m1=min(peak_ls)
m2=max(peak_ls)
m0=m2-m1
error_ls=[error_ls, m0]
endfor
writecol, 'run_II_SN.txt', file_ls, ls5, error_ls


stop
end
