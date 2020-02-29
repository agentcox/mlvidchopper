import os
import sys
import tscribe

if len(sys.argv) < 2:
	exit()

filetoparse = sys.argv[1]

tscribe.write(filetoparse)
