import csv
import math
import random
from datetime import datetime
from datetime import timedelta
from collections import defaultdict

pick_percent = 1.0
threshold_seconds = 3 #ignore all below this threshold
duration_end_buffer = 0 #add this number of seconds at end of every clip
inorder = True

csvfilename = '../timecodes/audiof14nightcapnewlighting.mp3.csv'
infile = '../in/f14nightcapnewlighting.mp4'
finaloutfile = '../out/f14nightcapnewlighting_finalcut_try1.mp4'
tempfileprefix = 'temp/cut'
concatinstructionsfile = 'concatinstruc.txt'

with open(csvfilename) as csvfile:
    reader = csv.reader(csvfile)
    reader.__next__()
    in_seq = [ row[0] for row in reader ]
with open(csvfilename) as csvfile:
    reader = csv.reader(csvfile)
    reader.__next__()
    dur_seq = [ row [2] for row in reader ]

arrnum = list(range(len(dur_seq)))
pickcount = math.floor(len(dur_seq) * pick_percent)
if pick_percent < 1.0:
    picknums = random.choices(arrnum, k=pickcount)
else:
    picknums = arrnum

if(inorder):
	picknums = sorted(picknums)

finalpicknums = []

#get rid of any that duration is < threshold
for num in picknums:
    dt = datetime.strptime(str(dur_seq[num]), '%H:%M:%S')
    dtime = dt.time()
    totalsec = dtime.hour * 360 + dtime.minute * 60 + dtime.second

    if(totalsec >= threshold_seconds):
    	finalpicknums.append(num)

deltasecs = timedelta(seconds=duration_end_buffer)

for i in range(len(finalpicknums)):
    stringout = 'ffmpeg -y -ss ' + str(in_seq[finalpicknums[i]]) + ' -i ' + infile + ' -t ' + str((datetime.strptime(dur_seq[finalpicknums[i]],'%H:%M:%S') + deltasecs).time()) + ' -c copy ' + tempfileprefix + str(i) + '.mp4'
    print(stringout)

##output the file instructions to the concat file
with open(concatinstructionsfile, 'w') as f:
	for y in range(len(finalpicknums)):
		filestr = "file '" + tempfileprefix + str(y) + '.mp4' + "'\n"
		f.write(filestr)

##now print the final concat operation
finalcutstr = "ffmpeg -y -hide_banner -f concat -i " + "\"" + concatinstructionsfile + "\"" + " -c copy " + finaloutfile

print(finalcutstr)
