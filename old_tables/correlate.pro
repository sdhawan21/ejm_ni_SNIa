;$Id: correlate.pro,v 1.26 2004/01/21 15:54:49 scottm Exp $
;
; Copyright (c) 1994-2004, Research Systems, Inc.  All rights reserved.
;       Unauthorized reproduction prohibited.
;+
; NAME:
;       CORRELATE
;
; PURPOSE:
;       This function computes the linear Pearson correlation coefficient
;       of two vectors or the Correlation Matrix of an M x N array.
;       Alternatively, this function computes the covariance of two vectors
;       or the Covariance Matrix of an M x N array.
;
; CATEGORY:
;       Statistics.
;
; CALLING SEQUENCE:
;       Result = Correlate(X [,Y])
;
; INPUTS:
;       X:    A vector or an M x N array of type integer, float or double.
;
;       Y:    A vector of type integer, float or double. If X is an M x N
;             array, this parameter should not be supplied.
;
; KEYWORD PARAMETERS:
;       COVARIANCE:    If set to a non-zero value, the sample covariance is
;                      computed.
;
;       DOUBLE:        If set to a non-zero value, computations are done in
;                      double precision arithmetic.
;
; RESTRICTIONS:
;       If X is an M x N array, then Y should not be supplied;
;       Result = Correlate(X)
;
; EXAMPLES:
;       Define the data vectors.
;         x = [65, 63, 67, 64, 68, 62, 70, 66, 68, 67, 69, 71]
;         y = [68, 66, 68, 65, 69, 66, 68, 65, 71, 67, 68, 70]
;
;       Compute the linear Pearson correlation coefficient of x and y.
;         result = correlate(x, y)
;       The result should be 0.702652
;
;       Compute the covariance of x and y.
;         result = correlate(x, y, /covariance)
;       The result should be 3.66667
;
;       Define an array with x and y as its columns.
;         a = [transpose(x), transpose(y)]
;       Compute the correlation matrix.
;         result = correlate(a)
;       The result should be [[1.000000,  0.702652]
;                             [0.702652,  1.000000]]
;
;       Compute the covariance matrix.
;         result = correlate(a, /covariance)
;       The result should be [[7.69697,  3.66667]
;                             [3.66667,  3.53788]]
;
; PROCEDURE:
;       CORRELATE computes the linear Pearson correlation coefficient of
;       two vectors. If the vectors are of unequal length, the longer vector
;       is truncated to the length of the shorter vector. If X is an M x N
;       array, M-columns by N-rows, the result will be an M x M array of
;       linear Pearson correlation coefficients with the iTH column and jTH
;       row element corresponding to the correlation of the iTH and jTH
;       columns of the M x N array. The M x M array of linear Pearson
;       correlation coefficients (also known as the Correlation Matrix) is
;       always symmetric and contains 1s on the main diagonal. The Covariance
;       Matrix is also symmetric, but is not restricted to 1s on the main
;       diagonal.
;
; REFERENCE:
;       APPLIED STATISTICS (third edition)
;       J. Neter, W. Wasserman, G.A. Whitmore
;       ISBN 0-205-10328-6
;
; MODIFICATION HISTORY:
;       Written by:  DMS, RSI, Sept 1983
;       Modified:    GGS, RSI, July 1994
;                    Added COVARIANCE keyword.
;                    Included support for matrix input.
;                    New documentation header.
;       Modified:    GGS, RSI, April 1996
;                    Included support for scalar and unequal length vector
;                    inputs. Added checking for undefined correlations and
;                    support of IEEE NaN (Not a Number).
;                    Added DOUBLE keyword.
;                    Modified keyword checking and use of double precision.
;   CT, RSI, Sept 2003: Force correlations to be in the range -1 to +1,
;           except for NaN values. Also force values on diagonal to be 1.
;
;-
FUNCTION Cov_Mtrx, X, Double = Double
  compile_opt hidden
  Nx = SIZE(x)
  double = keyword_set(double)
  if Double eq 0 then one = 1.0 else one = 1.0d
  if n_elements(x) le 1 then RETURN, one

  VarXi = X - (TOTAL(x,2, DOUBLE=double) # REPLICATE(one/nx[2], nx[2]))
  RETURN, matrix_multiply(VarXi, VarXi, /BT) / (nx[2]-1)
end

FUNCTION CRR_MTRX, X, Double = Double, N_NAN=nSS
  compile_opt hidden
  Nx = SIZE(x)
  double = keyword_set(double)
  if Double eq 0 then one = 1.0 else one = 1.0d
  if Nx[0] eq 0 or Nx[0] eq 1 then RETURN, one

  VarXi = x - (TOTAL(x,2, DOUBLE=double) # REPLICATE(one/nx[2], Nx[2]))
  SS = TOTAL(VarXi^2, 2)        ;Sum of squares of columns
  SS = SS # SS
  iSS = WHERE(SS eq 0, nSS)     ;Zero denominator signals undefined Correlation.
  if nSS ne 0 then begin
    SS[iSS] = one
    cm = Matrix_multiply(VarXi, VarXi, /BT)/SQRT(SS)
    cm[iSS] = !VALUES.F_NAN
    RETURN, cm
  endif else RETURN, Matrix_Multiply(VarXi, VarXi, /BT)/SQRT(SS)
end

FUNCTION Correlate, X, Y, Covariance = Covariance, Double = Double

  ON_ERROR, 2  ;Return to caller if an error occurs.

  if N_PARAMS() eq 2 then begin  ;Vector inputs.

    Sx = SIZE(x)  &  Sy = SIZE(y)
    if N_ELEMENTS(Double) eq 0 then $
      Double = (Sx[Sx[0]+1] eq 5) or (Sy[Sy[0]+1] eq 5)

    Nx = n_elements(x)
    Ny = n_elements(y)

    ;Means.
    sLength = Nx < Ny
    if nx le ny then begin
        xMean = TOTAL(X, Double = Double) / sLength
        xDev = X - xMean
    endif else begin
        tmp = x[0:ny-1]
        xMean = TOTAL(tmp, Double = Double) / sLength
        xDev = temporary(tmp) - xMean
    endelse

    if ny le nx then begin
        yMean = TOTAL(Y, Double = Double) / sLength
        yDev = Y - yMean
    endif else begin
        tmp = y[0:nx-1]
        yMean = TOTAL(tmp, Double = Double) / sLength
        yDev = temporary(tmp) - yMean
    endelse

    nan = KEYWORD_SET(Double) ? !VALUES.D_NAN : !VALUES.F_NAN
    if KEYWORD_SET(Covariance) eq 0 then begin  ;Correlation.
        dx2 = TOTAL(xDev^2, Double = Double)
        dy2 = TOTAL(yDev^2, Double = Double)
        if dx2 eq 0 or dy2 eq 0 then return, nan
        result = TOTAL(xDev * yDev, Double=Double) / (SQRT(dx2)*SQRT(dy2))
        return, -1 > result < 1
    endif else begin ;Covariance.
        if sLength eq 1 then return, nan
        return, TOTAL(xDev * yDev, Double = Double) / (sLength-1)
    endelse

  endif

    ;Array input.
    if N_ELEMENTS(Double) eq 0 then $
        Double = SIZE(x, /TYPE) eq 5

    if (KEYWORD_SET(Covariance)) then $
        return, COV_MTRX(X, Double = Double)

    ; Correlation.
    result = CRR_MTRX(X, Double = Double, N_NAN=nNaN)

    ; Make sure our correlation values are in -1 to +1 range.
    dim1 = (SIZE(x, /DIMENSIONS))[0]
    diag = LINDGEN(dim1)*(dim1 + 1)
    if (nNaN gt 0) then begin
        good = WHERE(FINITE(result), ngood)
        if (ngood gt 0) then $
            result[good] = -1 > result[good] < 1
        ; Because of roundoff error, values along diagonal are not always 1.
        ; So force them to be exactly 1. However, we need to preserve
        ; any NaN's, so only force the finite values to be 1.
        good = WHERE(FINITE(result[diag]), ngood)
        if (ngood gt 0) then $
            result[diag[good]] = 1
    endif else begin
        result = -1 > TEMPORARY(result) < 1
        ; Because of roundoff error, values along diagonal are not always 1.
        ; So force them to be exactly 1.
        result[diag] = 1
    endelse


  return, result

end

