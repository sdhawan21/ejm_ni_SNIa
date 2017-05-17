import rdlc as rl
import sys

if len(sys.argv)<2:
	print "Error: Please enter the filename of the SN \n Usage:"+sys.argv[0]+""



files=sys.argv[1]
sn=rl.rd_bol_data.nm(files)
lc=rl.rd_bol_data.rdlc(sn)
