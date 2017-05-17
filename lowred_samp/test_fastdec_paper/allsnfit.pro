pro allsnfit

ff=file_search('17/*.dat')
for i=0, n_elements(ff)-1 do begin
	mklcbol, ff[i]
	;t=cspline(wv, fl)
	;mklcbol, lc
endfor
stop
END
