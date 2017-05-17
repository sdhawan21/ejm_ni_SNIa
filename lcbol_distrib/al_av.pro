function al_av, lambda, r_v=rv, rverr=rverr, oldcoeff=oldcoeff

;Given wavelength (A) and R_V, return A_lambda/A_V assuming CCM89
;extinction law (with new coefficients from O'Donnell 1994
;unless /oldcoeff is set; see also ccm_unred.pro)
;2013-10-08: if rverr= is set, return [Al/Av,Al/Averr]

;if not keyword_set(r_v) then rv=3.1

x = 1e4/lambda ;convert to inverse microns

a=0.0 & b=0.0
if (x gt 0.3 and x lt 1.1) then begin ;IR
   a =  0.574 * x^(1.61)
   b = -0.527 * x^(1.61)
endif else if (x ge 1.1 and x lt 3.3) then begin ;optical/NIR
   y = x - 1.82
   if keyword_set(oldcoeff) then begin
      c1 = [ 1. , 0.17699, -0.50447, -0.02427,  0.72085,    $ ;Original
             0.01979, -0.77530,  0.32999 ]                    ;coefficients
      c2 = [ 0.,  1.41338,  2.28305,  1.07233, -5.38434,    $ ;from CCM89
             -0.62251,  5.30260, -2.09002 ]
   endif else begin
      c1 = [ 1. , 0.104,   -0.609,    0.701,  1.137,    $ ;New coefficients
             -1.718,   -0.827,    1.647, -0.505 ]         ;from O'Donnell
      c2 = [ 0.,  1.952,    2.908,   -3.989, -7.985,    $ ;(1994)
             11.102,    5.491,  -10.805,  3.347 ]
   endelse
   a = poly(y,c1)
   b = poly(y,c2)
endif else if (x ge 3.3 and x lt 8.) then begin ;mid-UV
   f_a=0. & f_b=0.
   if (x gt 5.9) then begin
      y = x-5.9
      f_a = -0.04473 * y^2 - 0.009779 * y^3
      f_b =   0.2130 * y^2  +  0.1207 * y^3
   endif
   a =  1.752 - 0.316*x - (0.104 / ( (x-4.67)^2 + 0.341 )) + f_a
   b = -3.090 + 1.825*x + (1.206 / ( (x-4.62)^2 + 0.263 )) + f_b
endif else if (x ge 8. and x le 11.) then begin ;far-UV
   y = x - 8.
   c1 = [ -1.073, -0.628,  0.137, -0.070 ]
   c2 = [ 13.670,  4.257, -0.420,  0.374 ]
   a = poly(y,c1)
   b = poly(y,c2)
endif

AlAv = a+b/rv
if n_elements(rverr) gt 0 then $
   return,[AlAv,AlAv*rverr/rv] else $
   return,AlAV

end
