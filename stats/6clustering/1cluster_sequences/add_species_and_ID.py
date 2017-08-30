import os
import sys


mymap = open('species_name_mapping', 'r')

for thing in mymap:
	ID = thing.strip().split('\t')[0]
	species = thing.strip().split('\t')[1]

	myfasta = open(ID + '_definedseqs_v5.fa', 'r')


	out = open(ID + '_definedseqs_v6.fa', 'w')


	for line in myfasta:
		if ">" in line:
			line = line.strip()+'|' + ID + '|' + species + '\n'
			out.write(line)
		else:
			out.write(line)