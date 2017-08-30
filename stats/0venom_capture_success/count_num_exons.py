import os
import sys
from collections import defaultdict

################ get number of exons per locus

myvenom = open('all_venom_bed', 'r')

mydict = dict()


for line in myvenom:
	info = line.strip().split('\t')

	if info[0] in mydict:

		mydict[info[0]] += 1
	else:
		
		mydict[info[0]] = 1

################## record values into a dictionary

genefamilydict = defaultdict(dict)


for item in mydict:
	genefamily = item.split('|')[2]



	if mydict[item] in genefamilydict[genefamily]:
		genefamilydict[genefamily][mydict[item]] += 1
	else:
		genefamilydict[genefamily][mydict[item]] = 1

for thing in sorted(genefamilydict):
	print thing, genefamilydict[thing]







