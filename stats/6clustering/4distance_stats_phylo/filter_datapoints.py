import os
import sys


myfile = open('all.datapoint', 'r')

out = open('all.datapoints.filtered', 'w')


for line in myfile:
	info = line.strip().split('\t')

	start1 = int(info[1])
	end1 = int(info[2])

	start2 = int(info[4])
	end2 = int(info[5])

	locuslengthmax = max(end1 - start1, end2 - start2)
	locuslengthmin = min(end1 - start1, end2 - start2)


	exonlength = int(info[8])
	intronlength = int(info[-3])
	alignlength = int(info[-1]) - int(info[-2])

	if float(alignlength)/float(locuslengthmax) > 1.2:
		continue

###### set min length for reasonable alignable intron length
	elif intronlength < 50:
		continue
	elif float(locuslengthmin)/float(locuslengthmax) < 0.7:
		continue

#	elif exonlength < locuslengthmax:
#		continue
#	elif float(info[-4]) > 0.4:
#		print line

#	elif float(info[-4]) - float(info[-2]) > 0.2:
#		print line
	else:
		out.write(line)


