import os
import sys
from Bio.Seq import translate


myfasta = open('all_extractedseq_renamed.fa', 'r')

fastadict = dict()

for line in myfasta:
	if ">" in line:
		fastadict[line.strip()[1:]] = next(myfasta).strip()

myconotoxins = open('conotoxins_predicted.txt', 'r')

out = open('conotoxins_functional_regions.bed', 'w')
for line in myconotoxins:
	info = line.strip().split('\t')

	if '|' in info[0]:

		name = info[0]

		myregions = [info[1], info[2], info[3], info[4]]

		mytypes = ['signal', 'pre', 'mature', 'post']


		endcounter = 0
		typecounter = 0
		for item in myregions:
			if item == '':
				typecounter += 1
				continue
			else:
				start = endcounter
				end = endcounter + len(item)*3

				print name
				print item
				print translate(fastadict[name][start:end])

				out.write(name + '\t' + str(start) + '\t' + str(end) + '\t' + mytypes[typecounter] + '\n')
				endcounter = end
				typecounter += 1

		



		