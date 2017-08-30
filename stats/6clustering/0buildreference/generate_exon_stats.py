import os
import sys
from collections import defaultdict
import numpy

######## get lengths

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




############### 



myvenombed = open('all_stats_venombed_annotated_v3', 'r')

venombeddict = defaultdict(dict)


for line in myvenombed:
	info = line.strip().split('\t')

	if len(info[0].split('|')) > 4:
		myID = '|'.join(info[0].split('|')[0:3]) + '|' + info[0].split('|')[3].split('_')[0]
		if info[5] == 'exon1':
			start = int(info[0].split('|')[4]) - int(info[0].split('|')[4])
			end = int(info[2]) - int(info[0].split('|')[4])
		elif info[5].replace('exon','') == info[6].replace('pieces',''):
			start = int(info[1]) - int(info[0].split('|')[4])
			end = int(info[0].split('|')[5]) - int(info[0].split('|')[4])
		else:
			start = int(info[1]) - int(info[0].split('|')[4])
			end = int(info[2]) - int(info[0].split('|')[4])

	else:
		myID = info[0]
		start = int(info[1])
		end = int(info[2])

	venombeddict[myID][info[6] + '|' + info[5]] = [start, end]


########### 

resultshistdict = defaultdict(dict)

resultsdict = defaultdict(dict)

myregions = open('conotoxins_functional_regions.bed', 'r')

mychecklist = []

mymatureexons = open('my.mature.exons.info', 'w')


for line in myregions:
	info = line.strip().split('\t')

	if info[0] in keeplist:
		mychecklist.append(info[0])

		genefamily = info[0].split('|')[2]

		regionname = info[-1]

		regionlist = range(int(info[1]), int(info[2]))

		mytemplist = []
		mytempdict = dict()

		for exon in sorted(venombeddict[info[0]]):
			exonlist = range(venombeddict[info[0]][exon][0], venombeddict[info[0]][exon][1])
			
			overlap = len(list(set(regionlist).intersection(exonlist)))


			if overlap > 0:
				percent_overlap = float(overlap)/float(len(regionlist))
				mytemplist.append(percent_overlap)
				mytempdict[genefamily+'|' + exon] = percent_overlap
				if genefamily +'|' + exon in resultsdict and regionname in resultsdict[genefamily + '|' + exon]:
					resultsdict[genefamily+'|' +exon][regionname].append(percent_overlap)


				else:
					resultsdict[genefamily+'|' +exon][regionname] = [percent_overlap]

		if regionname == 'mature':
			mymatureexons.write(max(mytempdict, key=mytempdict.get) + '\n')

		if regionname in resultshistdict:
			resultshistdict[regionname].append(max(mytemplist))
		else:
			resultshistdict[regionname] = [max(mytemplist)]	


out = open('region_distribution.stats','w')
out2 = open('region.distribution.forscripting.stats', 'w')
for item in sorted(resultsdict):
	signal = '-'
	pre = '-'
	mature = '-'
	post = '-'

	genefamily = item.split('|')[0]
	segment = item.split('|')[1].replace('1pieces', '1 segment').replace('pieces',' segments')
	exonnum = item.split('|')[2]

	for region in resultsdict[item]:
		if region == 'signal':
			signal = str(numpy.mean(resultsdict[item][region]))
		elif region == 'pre':
			pre = str(numpy.mean(resultsdict[item][region]))
		elif region == 'mature':
			mature = str(numpy.mean(resultsdict[item][region]))
		elif region == 'post':
			post = str(numpy.mean(resultsdict[item][region]))
		else:
			print 'fuck'


	myout = [genefamily, segment, exonnum, signal, pre, mature, post]
	myout2 = ['', '', exonnum, signal, pre, mature, post]
	myout3 = [genefamily, item.split('|')[1], exonnum, signal, pre, mature, post]
	
	out2.write('\t'.join(myout3) + '\n')

	if exonnum == 'exon1':

		out.write('\t'.join(myout) + '\n')

	else:
		out.write('\t'.join(myout2) + '\n')


histout = open('region_distribution_for_hist.stats', 'w')


for item in resultshistdict:
	histout.write(item + '\t' + '\t'.join([str(x) for x in resultshistdict[item]]) + '\n')

print len(list(set(keeplist)))
print len(list(set(mychecklist)))








