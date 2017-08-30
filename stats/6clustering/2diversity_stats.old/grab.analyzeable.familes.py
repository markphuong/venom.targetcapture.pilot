import os
import sys


myfile = open('diversity_stats_transposed.txt', 'r')

out = open('gene.family.sizes.stats' , 'w')

for line in myfile:
	if 'species' in line:
		out.write(line)
	elif 'exon 1' in line:
		info = line.strip().split('\t')

		print info[12]
		del info[12]

		if info.count('0') >= 6:
			continue
		else:
			out.write(line)



	
