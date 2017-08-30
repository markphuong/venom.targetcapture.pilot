import os
import sys
from collections import defaultdict


myfile = open('venom.datapoint', 'r')

out = open('venom.datapoints.filtered', 'w')




for line in myfile:
	info = line.strip().split('\t')

	start1 = int(info[0].split('|')[4])
	end1 = int(info[0].split('|')[5])

	start2 = int(info[1].split('|')[4])
	end2 = int(info[1].split('|')[5])

	locuslengthmax = max(end1 - start1, end2 - start2)
	locuslengthmin = min(end1 - start1, end2 - start2)


	exonlength = int(info[-5])
	intronlength = int(info[-3])

	alignlength = int(info[-1]) - int(info[-2])

	geneinfo = info[2]
#	print geneinfo
	family = geneinfo.split('.')[0]
	exon = geneinfo.split('.')[1]

	myoutput = line.strip() + '\t' + family + '\t' + exon + '\n'


	if float(alignlength)/float(locuslengthmax) > 1.2:
#		print line
#		print alignlength, locuslengthmax
		continue

###### set min length for reasonable alignable intron length
	elif intronlength < 50:
#		print line
		continue
	elif float(locuslengthmin)/float(locuslengthmax) < 0.7:
#		print line
#		print locuslengthmin, locuslengthmax
		continue
#	elif exonlength < locuslengthmax:
#		continue
#	elif float(info[-4]) > 0.4:
#		print line

#	elif float(info[-4]) - float(info[-2]) > 0.2:
#		print line
	else:
		out.write(myoutput)


out.close()

########### remove family if less than 50 comparisons

myfiltered = open('venom.datapoints.filtered', 'r')

counterdict = dict()

for line in myfiltered:
	info = line.strip().split('\t')

	family = info[-2] + '|' + info[-1]

	if family in counterdict.keys():
		counterdict[family] += 1
	else:
		counterdict[family] = 1

myfiltered.close()

savelist = []

for family in counterdict:
	if counterdict[family] < 50 or family == 'Q|mature':
		continue
	else:
		savelist.append(family)

myfiltered = open('venom.datapoints.filtered', 'r')
out = open('venom.datapoints.filtered.enoughdatapoints', 'w')

counterdict = dict()

for line in myfiltered:
	info = line.strip().split('\t')

	family = info[-2] + '|' + info[-1]

	if family in savelist:
		out.write(line)
	else:
		continue

out.close()

























