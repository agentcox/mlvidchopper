import csv
import math
import random
from datetime import datetime
from collections import defaultdict

pick_percent = 1.0
threshold_seconds = 3 #ignore all below this threshold
inorder = True
infile = 'in/danride_short.mp4'
finaloutfile = 'finalcut.mp4'
tempfileprefix = 'temp/cut'
concatinstructionsfile = 'concatinstruc.txt'

with open('test.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    reader.__next__()
    in_seq = [ row[0] for row in reader ]
with open('test.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    reader.__next__()
    dur_seq = [ row [2] for row in reader ]

arrnum = list(range(len(dur_seq)))
pickcount = math.floor(len(dur_seq) * pick_percent)
if pick_percent < 1.0:
    picknums = random.choices(arrnum, k=pickcount)
else:
    picknums = arrnum
#print(picknums)

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

for i in range(len(finalpicknums)):
    stringout = 'ffmpeg -y -ss ' + str(in_seq[finalpicknums[i]]) + ' -i ' + infile + ' -t ' + str(dur_seq[finalpicknums[i]]) + ' -c copy ' + tempfileprefix + str(i) + '.mp4'
    print(stringout)

##output the file instructions to the concat file
with open(concatinstructionsfile, 'w') as f:
	for y in range(len(finalpicknums)):
		filestr = "file '" + tempfileprefix + str(y) + '.mp4' + "'\n"
		f.write(filestr)

##now print the final concat operation
finalcutstr = "ffmpeg -y -hide_banner -f concat -i " + "\"" + concatinstructionsfile + "\"" + " -c copy " + finaloutfile

print(finalcutstr)