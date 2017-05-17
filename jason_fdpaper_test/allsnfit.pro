pro allsnfit

ff=file_search('filt/*.dat')
for i=0, n_elements(ff)-1 do begin
	mklcbol, ff[i]
	;t=cspline(wv, fl)
	;mklcbol, lc
endfor
stop
END
