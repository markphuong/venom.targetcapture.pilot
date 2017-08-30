import os
import sys
from collections import defaultdict

def checkoverlap(a, b):
	overlap = max(0, min(a[1], b[1]) - max(a[0], b[0]))
        length1 = len(range(a[0],a[1]+1))

	length2 = len(range(b[0],b[1]+1))

	ratio1 = float(overlap)/length1
	ratio2 = float(overlap)/length2

	return max(ratio1, ratio2)


################## for all the loci in rbbh, write out the blast lines for the rbbh and other non overlapping regions (threshold is max 20% overlap between any two fragments that are already kept)



out = open(sys.argv[2], 'w')
mytblastn = open(sys.argv[1], 'r')

blastcoorddict = defaultdict(list)

for line in mytblastn:
	info = line.strip().split('\t')


#	if '|T|' in info[1]:
	if info[0] in blastcoorddict:
		mycoords = [int(info[6]), int(info[7])]	

		keep = 'yes'

		for mylist in blastcoorddict[info[0]]:
			if checkoverlap(mycoords, mylist) > .05:
				keep = 'no'
			else:
				continue
		if keep == 'yes':
			out.write(line)
			blastcoorddict[info[0]].append(mycoords)
		else:
			continue
	
	else:
		blastcoorddict[info[0]] = [[int(info[6]),int(info[7])]]
		out.write(line)
#	else:
#		continue


out.close()
