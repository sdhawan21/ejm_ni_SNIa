;$Id: mean.pro,v 2.8 2011/04/08 20:23:26 haimov Exp haimov $
;+
; NAME:
;       MEAN
; PURPOSE:
;       Returns mean value for a random variable X.
; CALLING SEQUENCE:
;       result=mean(x, dim, double=double,nan=nan,silent=silent,help=help)
; INPUTS:
;       X:    input array (any numerical type)
;       Dim:  the array dimension over which to calculate mean, starting from 1
;             If DIM=0 or not present mean for the whole array is calculated.
; OUTPUTS:
;       The result is a scalar for DIM=0 or not present. For DIM > 0 the result
;       is an array with one less dimension than X.  For LONG, DOUBLE, DCOMPLEX,
;       ULONG, LONG64, or ULONG64 the result is DOUBLE; for BYTE, INT, FLOAT it
;       is FLOAT; and for the complex types it matches the type.
;
; KEYWORD PARAMETERS:
;       DIMENSION: same as Dim input; it is ignored if Dim is non-zero
;                  Note: IDL added DIMENSION keyword in their IDL 8.0 version
;                        It is added here to maintain compatibility.
;       DOUBLE: if set to a non-zero value, computations are done in
;               double precision arithmetic (this is include for compatibility
;               with the IDL mean routine added with IDL version 5.1)
;       NAN:    when set, NaNs in X are treated as missing values
;       SILENT: when set, information messages are suppressed
;       HELP:   prints this help
;
; SIDE EFFECTS:      
;
;       The function returns NaN when no finite values are found for
;       the averaged array or part of the array regardless if NAN
;       keyword is set or not.
;      
;       The function returns empty string '' if X is non-numerical.
;
;       When NAN keyword is set but there are no valid data (all values
;       are NaN or Inifinity) the result is NaN.
;
; NOTES:
;       print,mean() prints out the usage
;
;       Same name function was added to standard IDL library with idl 5.1. 
;       This kind of name conflicts are always possible thus it is a good 
;       practice for the user to arrange the IDL path in an order where the
;       desired routines with duplicated names are found first.
;
;       It may be useful to be reminded that when an array is assembled
;       using numerical data of different types there is precedence that
;       determines the type of the array. For example if you try to use
;       !values.f_nan as missing values in an array of long integers the
;       array will be converted to float and some of the long integers
;       in single precision float may not be correct. 
;-    
; MODIFICATION HISTORY:
;       Samuel Haimov, Dec 1995
;       SH, Jul 1996 -- added nan keyword
;       SH, Nov 1996 -- added input parameter dim
;       SH, Oct 1997 -- minor changes
;       SH, Oct 1999 -- note about same name idl function introduced in v5.1
;       SH, Jan 2003 -- allowed the input to be scalar
;       SH, Jul 2006 -- added silent keyword; modified ro work with all
;                       integer types; did some mods to make it behave better
;                       when NaN values are present and NAN keyword is used
;       SH, Aug 2007 -- added DOUBLE keyword for compatibility with IDL mean
;                       function introduced with IDL 5.1 version
;       SH, Dec 2010 -- added DIMENSION keyword to maintain compatibility
;                       with the version 8.0 updated native IDL mean function.
;                         
; Copyright (C) 1996-2005, Samuel Haimov, Dept. of Atmos. Sci., University of
; Wyoming.  This software may be used, copied, or redistributed as long as it 
; is not sold and this copyright notice is reproduced on each copy made. This
; routine is provided as is without any expressed or implied warranties
; whatsoever.  Other limitations apply as described in the Readme file.
;

function mean, x, dim, dimension=dimension,double=double,nan=nan,silent=silent,$
                       help=help

on_error,2

if KEYWORD_SET(help) then begin
  doc_library,'mean'
  return,''
endif

  xtype=size(x,/type)

; Check input

  if n_params() eq 0 then begin
     message,'Usage: result=mean(x,dim,double=double,nan=nan)',/info
     return,''
  endif else if n_params() eq 1 then dim=0 $
  else if dim lt 0 or dim gt size(x,/n_dimension) then $
    message,'Incorrect input value for Dim.'

  if n_elements(dimension) eq 1 and dim eq 0 then begin
    if dimension lt 0 or dimension gt size(x,/n_dimension) then $
    message,'Illegal keyword value for DIMENSION.'
    dim=dimension
  endif
  
  if (xtype eq 0 or xtype eq 7 or xtype eq 8 or xtype eq 10 or xtype eq 11) $
  then begin
     if not keyword_set(silent) then message,'Invalid argument type.',/info
     return,''
  endif else ytype=4*(xtype eq 1 or xtype eq 2 or xtype eq 4 or xtype eq 12)+$
     5*(xtype eq 3 or xtype eq 5 or xtype eq 13 or xtype eq 14 or xtype eq 15)+$
     6*(xtype eq 6)+9*(xtype eq 9)

  if (n_elements(x) eq 1) then begin        
     if not keyword_set(silent) then $
       message,'Scalar input; return same value.',/info
     return,x
  endif

; Compute mean

  xmean=total(x,dim,nan=nan,double=double)
  junk=total(finite(x),dim,double=double)

  ind=where(junk eq 0,compl=ind1)
  if ind[0] ne -1 then xmean[ind]=!values.f_nan
  if ind1[0] ne -1 then xmean[ind1]=xmean[ind1]/junk[ind1]

return,fix(xmean,type=ytype)

end
