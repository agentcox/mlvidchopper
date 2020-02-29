import os
import sys
import createcsvfromtranscriptjson

if len(sys.argv) < 2:
	exit()

filetoparse = sys.argv[1]

createcsvfromtranscriptjson.write(filetoparse)
