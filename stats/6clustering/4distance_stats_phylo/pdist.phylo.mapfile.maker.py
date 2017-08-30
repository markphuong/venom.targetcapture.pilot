import os
import sys
from collections import defaultdict


def pdist(seq1, seq2):
	"""Sequences must be strings, have the same length, and be aligned"""
	num = 0
	diff = 0
	for i, nucleotide in enumerate(seq1):
		couple = [nucleotide, seq2[i]]
		if couple[0] == "-" or couple[0] == 'N':
			continue
		elif couple[1] == "-" or couple[1] == 'N':
			continue
		elif couple[0] == couple[1]:
			num += 1
		elif not couple[0] == couple[1]:
			num += 1
                        diff += 1
	if num == 0:
		return ['NA', '0']
	else:

		pdist = float(diff)/float(num)
		return [pdist,num]


myfasta = open('all_cut_up_exons_plus_introns.fa', 'r')

fastadict = defaultdict(dict)

for line in myfasta:
	if ">" in line:
		info = line.strip()[1:].split('|')

		species = info[0]

		locus = '|'.join(info[4:])

		start = int(info[2])
		end = int(info[3])

		fastadict[species][locus] = [next(myfasta).strip(), start, end]


counter = 0
out = open('mapfile', 'w')

alreadydone = []

for ID1 in fastadict:
	for ID2 in fastadict:
		if ID1 + '---' + ID2 in alreadydone or ID2 + '---' + ID1 in alreadydone or ID1 == ID2:
			continue
		elif ID1 == ID2:
			continue
		else:

###### save comparison as done
			alreadydone.append(ID1 + '---' + ID2)
			alreadydone.append(ID2 + '---' + ID1)

############# loop over all loci

			locuslist1 = fastadict[ID1].keys()
			locuslist2 = fastadict[ID2].keys()

			locilist = set(locuslist1).intersection(locuslist2)
		#	out = open("mapfile" + str(counter),'w')
			for locus in locilist:


				out.write(ID1 + '\t' + ID2 + '\t'  + locus + '\n')
			

		#	out.close()
			counter += 1




















		


























