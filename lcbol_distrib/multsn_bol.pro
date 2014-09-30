pro multsn_bol

ff=file_search('../SN*BVRIJH.dat')
lc=ff[0]
nmarr=['SN2005hc', 'SN2008bc', 'SN2008gp']
yarr=['SN2005iq', 'SN2005ki', 'SN2005al', 'SN2006bh']
for i=0, n_elements(yarr)-1 do begin
	mklcbol, '../ybollc/'+yarr(i)+'_lc_bol.dat'
	;t=cspline(wv, fl)
	;mklcbol, lc
endfor
stop
END
