pro evalidl

readcol, '../plot_rel/scr/lbol_t2_j.txt', nm, t2, et2, lb, elb, FORMAT='A, F, F ,F, F' 
linmix_err, t2, lb, post, xsig=et2, ysig=elb
save, post, FILENAME='slpval.sav'
stop
end
