import os
import sys
from collections import defaultdict
import numpy
from operator import itemgetter
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


myfasta = open('all_extractedseq_renamed.fa', 'r')

keeplist = []

for line in myfasta:
	if ">" in line:
		info = line.strip().split('|')
		seq = next(myfasta).strip()

		if line.strip()[1:] in counterdict:
			if float(counterdict[line.strip()[1:]])/float(len(seq)) > .8:
				keeplist.append(line.strip()[1:])


#####################

myblast = open('all_stats_venombed_annotated_v3', 'r')

myrealIDs = []

for line in myblast:
	info = line.strip().split('\t')


	if len(info[0].split('|')) > 4:
		myID = '|'.join(info[0].split('|')[0:3]) + '|' + info[0].split('|')[3].split('_')[0]

	else:
		myID = info[0]

	if myID in keeplist:
		myrealIDs.append(info[0])

myblast.close()

############################# LABEL REGIONS


################# get bed info

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

removelist = []

regiondict = defaultdict(dict)

myregions = open('conotoxins_functional_regions.bed', 'r')

mychecklist = []

alreadydone = []
for line in myregions:
	info = line.strip().split('\t')

	if info[0] in keeplist:
		mychecklist.append(info[0])

		genefamily = info[0].split('|')[2]

		regionname = info[-1]

		regionlist = range(int(info[1]), int(info[2]))

		mytemplist = []
		mytempdict = dict()

		tempdict = dict()


		if len(venombeddict[info[0]]) == 1:
			for exon in venombeddict[info[0]]:
				regiondict[info[0]]['onepiece'] =exon

		elif regionname == 'signal' or regionname == 'mature':

			for exon in sorted(venombeddict[info[0]]):
				exonlist = range(venombeddict[info[0]][exon][0], venombeddict[info[0]][exon][1])
			
				overlap = len(list(set(regionlist).intersection(exonlist)))



				percent_overlap = float(overlap)/float(len(regionlist))
	
				mytempdict[genefamily+'|' + exon] = percent_overlap

## Mark, double check here

			if info[0] + '|' +max(mytempdict, key=mytempdict.get) in alreadydone:
				removelist.append(info[0])
			else:
				regiondict[info[0]][regionname] = max(mytempdict, key=mytempdict.get)
				alreadydone.append(info[0] + '|' +max(mytempdict, key=mytempdict.get))


########### 

for item in removelist:
	del regiondict[item]

print removelist

##################

myblastdict = defaultdict(dict)

myblastcoord = open(sys.argv[1], 'r')

for line in myblastcoord:
	info = line.strip().split('\t')

	if info[0] in myrealIDs:

		if info[0] in myblastdict:
			myblastdict[info[0]].append([int(info[6]), int(info[7]), info[1]])
		else:
			myblastdict[info[0]]= [[int(info[6]), int(info[7]), info[1]]]

myblastcoord.close()


myblastcoord = open(sys.argv[2], 'r')

for line in myblastcoord:
	info = line.strip().split('\t')

	if info[0] in myrealIDs:


		if info[0] in myblastdict:
			myblastdict[info[0]].append([int(info[6]), int(info[7]), info[1]])
		else:
			myblastdict[info[0]]= [[int(info[6]), int(info[7]), info[1]]]

################################## get fastas

myfasta = open(sys.argv[3], 'r')

fastadict = dict()

for line in myfasta:
	if ">" in line:
		fastadict[line.strip()[1:]] = next(myfasta).strip()


#####################################

#print regiondict


print regiondict['Vi_O2_12|virgo|O2|6613.67757009']
#print len(regiondict['Vr_B4_2|varius|B4|2797.42105263'])

mybed = open(sys.argv[4], 'r')

out = open(sys.argv[5], 'w')


for line in mybed:
	info = line.strip().split('\t')

	exon = info[5]
	pieces = info[6]


	if len(info[0].split('|')) > 4:
		mybedID = '|'.join(info[0].split('|')[0:3]) + '|' + info[0].split('|')[3].split('_')[0]
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
		mybedID = info[0]

		start = int(info[1])
		end = int(info[2])


	if 'didnotblast' in line or not info[0] in myrealIDs:
		continue
	elif info[0] in myrealIDs and mybedID in regiondict:
		myregion = ''

		if len(regiondict[mybedID]) == 1:
			if 'onepiece' in regiondict[mybedID]:
				myregion = 'onepiece'
			else:
				print regiondict[mybedID]
		elif len(regiondict[mybedID]) == 2:

			exonlist = []
			for item in regiondict[mybedID]:
				exonlist.append(int(regiondict[mybedID][item].split('|')[-1].replace('exon','')))
				if exon in regiondict[mybedID][item]:
					myregion = item
				else:
					myregion = myregion
			if myregion == '':
				if int(exon.replace('exon','')) > sorted(exonlist)[-1]:
					myregion = 'post'
				else:
					myregion = 'pre'
	else:
		out.write(line.strip() + '\t' + 'FAILED' + '\t' + 'FAILED' + '\n')
		continue

#	print info[0]

#	if 'Vi11.2|virgo|I2|18714.7336449' == info[0]:
#		print myregion

	written = ''

	for item in myblastdict[info[0]]:
		rangeblast = range(item[0], item[1])
		rangeexon = range(start, end)

		overlap = len(list(set(rangeblast).intersection(rangeexon)))

		percent_overlap = float(overlap)/float(len(rangeexon))


		if percent_overlap > .3:
			out.write(line.strip() + '\t' + myregion + '\t' + item[2] + '\n')
			written = 'yes'
	if written == 'yes':
		continue
	else:
		out.write(line.strip() + '\t' + 'FAILED' + '\t' + 'FAILED' + '\n')

















