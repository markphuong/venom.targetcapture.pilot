import os
import sys

myblast = open('selfblast.venomblast', 'r')


clusterlist = []

for line in myblast:
	info = line.strip().split('\t')

	if '|A|' in info[0] and not 'exon1' in info[0]:
		clusterlist.append(info[1])



print set(clusterlist)

print len(list(set(clusterlist)))