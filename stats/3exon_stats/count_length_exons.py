import os
import sys
from collections import defaultdict
import numpy

######### get lengths

myblast = open('all_stats_venombed_annotated_v3', 'r')

counterdict = dict()

for line in myblast:
	info = line.strip().split('\t')

	if len(info[0].split('|')) > 4:
		myID = '|'.join(info[0].split('|')[0:3]) + '|' + info[0].split('|')[3].split('_')[0]
		if info[5] == 'exon1':
			start = int(info[0].split('|')[4])
			end = int(info[2])
		elif info[5].replace('exon','') == info[6].replace('pieces',''):
			start = int(info[1])
			end = int(info[0].split('|')[5])
		else:
			start = int(info[1])
			end = int(info[2])

	else:
		myID = info[0]
		start = int(info[1])
		end = int(info[2])

#	print myID
#	print start
#	print end

	if 'didnotblast' in line:
		continue
	else:
		if myID in counterdict.keys():
			counterdict[myID] += len(range(start, end))

		else:
			counterdict[myID] = len(range(start, end))


myblast.close()

###### generate list of sequences to keep. at least 80% of the sequence has to have been blasted.


myfasta = open('all_extractedseq_merged.fa', 'r')

keeplist = []

for line in myfasta:
	if ">" in line:
		info = line.strip().split('|')
		seq = next(myfasta).strip()

		if line.strip()[1:] in counterdict:
			if float(counterdict[line.strip()[1:]])/float(len(seq)) > .8:
				keeplist.append(line.strip()[1:])


################ get length per locus

myvenom = open('all_stats_venombed_annotated_v3', 'r')

resultsdict = dict()


for line in myvenom:
	info = line.strip().split('\t')

	if len(info[0].split('|')) > 4:
		myID = '|'.join(info[0].split('|')[0:3]) + '|' + info[0].split('|')[3].split('_')[0]
		if info[5] == 'exon1':
			start = int(info[0].split('|')[4])
			end = int(info[2])
		elif info[5].replace('exon','') == info[6].replace('pieces',''):
			start = int(info[1])
			end = int(info[0].split('|')[5])
		else:
			start = int(info[1])
			end = int(info[2])

	else:
		myID = info[0]
		start = int(info[1])
		end = int(info[2])

	mykey = myID.split('|')[2] + '|' + info[6] + '|' + info[5]

	if myID in keeplist:
		if mykey in resultsdict:
			resultsdict[mykey].append(end-start)
		else:
			resultsdict[mykey] = [end-start]			

########### write out results

out = open('exon_lengths.stats', 'w')

for key in sorted(resultsdict.keys()):

	info = key.split('|')
	genefamily = info[0]
	pieces = info[1]
	exon = info[2]

	mymin = str(min(resultsdict[key]))
	mymax = str(max(resultsdict[key]))
	average = str(numpy.mean(resultsdict[key]))

	out.write('\t'.join([genefamily, pieces, exon, average, mymin + ' - ' + mymax]) + '\n')










