;Use linmix_err by Kelly to evaluate the posterior
;use python script in 'src/' to analyse the output
;output save file 
PRO eval_slp

readcol, 'out_files/err_bivar_regress.txt', sn, lmax, el, y, ey, j, ej, FORMAT='A, F, F, F, F, F, F'

linmix_err, j, lmax, post, xsig=ej, ysig=el

save, post, filename='output_kelly.sav'

stop
end
