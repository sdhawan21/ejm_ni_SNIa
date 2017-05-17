from numpy import *
from glob import glob
fil=sorted(glob('srctex/*'))
#fil=glob('2011fe_ir.txt')
for f in fil:
   lc=open(f, 'r')
   fout=open('fin_lc/'+f[7:len(f)], 'w')
   ls=[]
   for row in lc:
       ls.append(row.split())
   for i in ls:
       for j in i:
           if j=='&':
               fout.write(' ')
           elif '(' in j:
               p=j.index('(')
               k=j[1:len(j)-1]
               #l=float(k)/1000
               if len(j)>8:
                   fout.write(j[0:p]+'\t')
               fout.write(k+'\t')
           elif 'd' in j:
               fout.write('99\t99\t')
           else:
               fout.write(j+'\t')
       fout.write('\n')
   fout.close()
