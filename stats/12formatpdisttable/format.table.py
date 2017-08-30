import os
import sys
from collections import defaultdict


myfile = open('mymeans.txt', 'r')


mydict = defaultdict(dict)

headerlist = []

for line in myfile:
	info = line.strip().split('\t')

	family = info[0]
	headerlist.append(info[1])

	mydict[family][info[1]] = info[2]


out = open('formatted.pdist.table', 'w')

output = ['family']

for header in sorted(set(headerlist)):
	output.append(header)

out.write('\t'.join(output) + '\n')



for thing in sorted(mydict):
	output = [thing]
	for header in sorted(set(headerlist)):
		if header in mydict[thing].keys():
			output.append(mydict[thing][header])
		else:
			output.append('-')
	out.write('\t'.join(output) + '\n')




