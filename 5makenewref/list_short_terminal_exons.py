import os
import sys

mybed = open('all_venombed_annotated', 'r')

out = open('short_terminal_exons.list', 'w')

for line in mybed:
	info = line.strip().split('\t')

	if 'didnotblast' in line:
		start = int(info[1])
		end = int(info[2])
		exon = info[5]
		pieces = info[6]

		if exon == 'exon1' and len(range(start,end)) < 40:
			out.write(line)

		elif exon.replace('exon','') == pieces.replace('pieces','') and len(range(start,end)) < 40:
			out.write(line)
