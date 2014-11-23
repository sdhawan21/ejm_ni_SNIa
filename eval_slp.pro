PRO eval_slp

readcol, 'out_files/err_bivar_regress.txt', sn, lmax, el, y, ey, j, ej, FORMAT='A, F, F, F, F, F, F'

linmix_err, j, lmax, post, xsig=ej, ysig=el

stop
end
