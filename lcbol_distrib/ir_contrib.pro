pro ir_contrib

readcol, "../tables/u_flags.txt", nm, FORMAT="A"
nm1=nm[where (nm ne "SN")]

ff=file_search('../ybollc/*.dat')
for j=0, 1 do begin
	for i=6, n_elements(ff)-1 do begin
		bolfile=ff[i]	
		mklcbol, bolfile
	endfor
endfor


;writecol, "../out_files/ir_frac.txt", ls

stop
end
