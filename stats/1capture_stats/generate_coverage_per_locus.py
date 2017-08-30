import os
import sys
import numpy
from collections import defaultdict


#################################### get dictionary of the overlappers


myremoved = open('removed_overlappers', 'r')

removed = defaultdict(list)

for line in myremoved:
	info = line.strip().split('\t')

	if info[0] in removed.keys():
		removed[info[0]].append('\t'.join(info[2:]))
	else:
		removed[info[0]] = ['\t'.join(info[2:])]


####################### load dictionary of coverage

ID = sys.argv[1]

mycov = open(ID + '_capstats.cov', 'r')

covdict = dict()

for line in mycov:
	info = line.strip().split('######')

	covlist = info[1][1:-1].split(', ')

	covlist = [int(item) for item in covlist]
	covdict[info[0]] = covlist
	

####################### load dictionary of sequences
myfasta = open(sys.argv[1] + '_venom_phylo_combined.fa', 'r')

fastadict = dict()
headerlist=[]

for line in myfasta:
	if ">" in line:

		header = line.strip()[1:]
		headerlist.append(header)
		seq = next(myfasta).strip()
		fastadict[header] = seq


myfasta.close()
################ some contigs may not show up in the VCF file, so you have to create lists of 0's and put them in your cov and het dictionaries

for item in set(headerlist):
	if item in covdict.keys():
		continue
	else:
		covdict[item] = [0]*4000

############################################################################




out = open(ID + '_coverage', 'w')


for item in sorted(fastadict):

	header = item
	seq = fastadict[item]

	if 'seed' in header:

		start = int(header.split('|')[-3])
		end = int(header.split('|')[-2])

		mysubset = covdict[header][start:end]

		out.write(header + '\t' +str(numpy.mean(mysubset)) + '\n')
	else:
		continue


myblast = open(ID + '_6.1_filtered_recipblast', 'r')

lengthout = open(ID + '_totallength', 'w')

mylength = 0

for line in myblast:
	info = line.strip().split('\t')


	if line.strip() in removed[ID]:
		continue

	else:

		if int(info[8]) > int(info[9]):
			start = int(info[9])
			end = int(info[8])
		else:
			start = int(info[8])
			end = int(info[9])



		thecov = covdict[info[1]][start-1:end]

		mylength += len(thecov)	
		
		out.write(info[0] + '\t' + info[1] + '\t' +str(numpy.mean(thecov)) + '\n')		

lengthout.write(ID + '\t' + str(mylength) + '\n')




















