import os
import sys
from collections import defaultdict

myfile = open('diversity_stats_transposed.txt', 'r')

mydict = defaultdict(dict)

out = open('diversity.stats.for.figure.s1', 'w')


reference = {'signal': 0, 'pre':1, 'mature': 2, 'post' : 3, 'onepiece' : 4}

for line in myfile:
	info = line.strip().split('\t')

	if info[0] == 'species':
		out.write(line)

	else:
		family = info[0].split('_')[0]

		region = info[0].split('_')[1]
		
		if family in mydict:
			mydict[family].append([reference[region], line])
		else:
			mydict[family] = [[reference[region],line]]



for family in sorted(mydict):

	for item in sorted(mydict[family]):
		output = item[1].replace('_',' ').replace('pre','prepro').replace('onepiece', 'single exon')
		out.write(output)
