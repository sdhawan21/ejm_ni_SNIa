function getplotpos, nxplot, nyplot,$
                     xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax,$
                     vspace=vspace, hspace=hspace

;returns structure of plot positions

;defaults
if not keyword_set(xmin) then xmin=.10
if not keyword_set(ymin) then ymin=.10
if not keyword_set(xmax) then xmax=.90
if not keyword_set(ymax) then ymax=.90
if not keyword_set(vspace) then vspace=0.
if not keyword_set(hspace) then hspace=0.

;output structure
nplot = nxplot * nyplot
pos = {x0:fltarr(nplot),x1:fltarr(nplot),y0:fltarr(nplot),y1:fltarr(nplot)}

;x,y sizes of individual plots
dxplot = (xmax-xmin-(nxplot-1.)*hspace)/float(nxplot)
dyplot = (ymax-ymin-(nyplot-1.)*vspace)/float(nyplot)

pos.x0 = xmin + rebin(indgen(nxplot),nxplot,nyplot) * (dxplot+hspace)
pos.x1 = xmin + rebin(indgen(nxplot)+1,nxplot,nyplot) * dxplot + rebin(indgen(nxplot),nxplot,nyplot) * hspace
pos.y0 = ymax - transpose(rebin(indgen(nyplot)+1,nyplot,nxplot)) * dyplot - transpose(rebin(indgen(nyplot),nyplot,nxplot)) * vspace
pos.y1 = ymax - transpose(rebin(indgen(nyplot),nyplot,nxplot)) * (dyplot+vspace)

return,pos
end
