import os
import sys

majority = open('majority_num_exons.reference', 'r')

keepdict = dict()

for line in majority:
	info = line.strip().split('\t')

	keepdict[info[0]] = info[1] + 'pieces'


out = open('venom_diversity_stats.reference.fa','w')

mapfile = open('mapfile', 'r')

mypieces = []

for line in mapfile:
	info = line.strip().split('\t')

	ID = info[0]
	species = info[1]


	fastadict = dict()


	myfasta = open(ID + '_definedseqs_v5.fa', 'r')

	for line in myfasta:
		if ">" in line:
			fastadict[line.strip()[1:]] = next(myfasta).strip()

	myfasta.close()

	mybed = open(species + '_venomblastcoordfile_annotated', 'r')

	alreadyseen = []

	for line in mybed:
		info = line.strip().split('\t')

		genefamily = info[0].split('|')[2]
		pieces = info[-1]

		if info[1] in alreadyseen:
			continue

		elif genefamily in keepdict and pieces == keepdict[genefamily]:
			alreadyseen.append(info[1])
			out.write('>' + species + '|' + info[1] + '|' + genefamily + '|' + info[-2] + '|' + pieces + '\n')
			out.write(fastadict[info[1]] + '\n')
			mypieces.append(genefamily + '_' + info[-2] + '_' + pieces)
		else:
			continue


out2 = open('mapfile.venomgenes', 'w')

for item in sorted(list(set(mypieces))):
	out2.write(item + '\n')






















