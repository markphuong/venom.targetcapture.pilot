import os
import sys
from collections import defaultdict


regiondict = defaultdict(dict)

myregions = open('testfile', 'r')

pieceslist = []

for line in myregions:
	info = line.strip().split('\t')

	genefamily = info[0]

	pieces = info[1]

	exon = info[2]

	signal = info[3]
	pre = info[4]
	mature = info[5]
	post = info[6]

	regiondict[genefamily+'|'+pieces+'|'+exon]['signal'] = signal
	regiondict[genefamily+'|'+pieces+'|'+exon]['pre'] = pre
	regiondict[genefamily+'|'+pieces+'|'+exon]['mature'] = mature
	regiondict[genefamily+'|'+pieces+'|'+exon]['post'] = post

	pieceslist.append(genefamily + '|' + pieces)

pieceslist = list(set(pieceslist))

regionlist = ['signal', 'pre', 'mature', 'post']

for family in pieceslist:

	tempdict = dict()

	exonlist = []

	for key in regiondict:
		if family in key:
			exonlist.append(key.split('|')[2])
			for region in regionlist:
				if region in tempdict:
					tempdict[region].append(regiondict[key][region])
					
				else:
					tempdict[region] = [regiondict[key][region]]

	badlist = ['-']

	finaldict = dict()

	for item in tempdict:
		tempdict[item] = [float(x) for x in tempdict[item] if x not in badlist]

		if len(tempdict[item]) == 0:
			continue
		else:
			finaldict[item] = max(tempdict[item])

	for exon in exonlist:
		mykey = family + '|' + exon
		print mykey