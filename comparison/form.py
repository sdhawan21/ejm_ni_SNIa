import numpy as np
import sys

def scalzo_ni(mb):
	return pow(10, -0.4*(mb+19.841))

def main():
	mb=float(sys.argv[1])
	ni=scalzo_ni(mb)
	print ni

main()
