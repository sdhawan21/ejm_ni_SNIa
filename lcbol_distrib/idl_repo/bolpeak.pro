pro bolpeak

ff=file_search("../finfiles/utest/*")
pk_arr=[]			;define array to store peak values 
for i=0, n_elements(ff)-1 do begin
	readcol, ff(i), mj, fl, flerr, format="F LL LL"
	cs=cspline(mj, fl, mj)
	print, mj[0], fl[0]
endfor
print, n_elements(ff)
stop
end

