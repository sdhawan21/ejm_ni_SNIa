pro multsn_bol

ff=file_search('../lowred_samp/*_bol.dat')
lc=ff[0]
print, ff[1]
for i=0, n_elements(ff)-1 do begin
	mklcbol, ff[i]
	;t=cspline(wv, fl)
	;mklcbol, lc
endfor
stop
END
