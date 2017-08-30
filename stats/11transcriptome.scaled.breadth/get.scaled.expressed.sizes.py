import os
import sys
from collections import defaultdict

all = []

file1 = open('gene.family.sizes.all', 'r')

for line in file1:
	if 'exon' in line:
		info = line.strip().split('\t')
		all.append(info[0].split(' ')[0])

sevpercent = []

file2 = open('gene.family.sizes.70percent', 'r')

for line in file2:
	if 'exon' in line:
		info = line.strip().split('\t')
		sevpercent.append(info[0].split(' ')[0])

captureable = []

file3 = open('gene.family.sizes.captureable', 'r')

for line in file3:
	if 'exon' in line:
		info = line.strip().split('\t')
		captureable.append(info[0].split(' ')[0])


mydict = defaultdict(dict)


myfasta = open('total_unique_mature_toxins_extractedseq.fa', 'r')

for line in myfasta:
	if ">" in line:
		info = line.strip().split('|')

		species = info[1]

		family = info[2]

		if species in mydict:

			if family in captureable:
				mydict[species]['captureable'] += 1
			if family in sevpercent:
				mydict[species]['sevpercent'] += 1	
			if family in all:
				mydict[species]['all'] += 1

			mydict[species]['total'] += 1
		else:
			mydict[species]['captureable'] = 0
			mydict[species]['sevpercent'] = 0
			mydict[species]['all'] = 0


			if family in captureable:
				mydict[species]['captureable'] = 1

			if family in sevpercent:
				mydict[species]['sevpercent'] = 1

			if family in all:
				mydict[species]['all'] = 1


			mydict[species]['total'] = 1


out = open('my.expressed.venom' ,'w')


for species in sorted(mydict):
	output = [species]
	for item in sorted(mydict[species]):
		print item
		output.append(str(mydict[species][item]))

	out.write('\t'.join(output) + '\n')












