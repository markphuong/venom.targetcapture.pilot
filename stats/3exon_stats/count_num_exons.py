import os
import sys
from collections import defaultdict
import operator
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


################ get number of exons per locus

myvenom = open('all_stats_venombed_annotated_v3', 'r')

mydict = dict()


for line in myvenom:
	info = line.strip().split('\t')

	if len(info[0].split('|')) > 4:
		myID = '|'.join(info[0].split('|')[0:3]) + '|' + info[0].split('|')[3].split('_')[0]

	else:
		myID = info[0]


	if myID in mydict:

		mydict[myID] += 1
	else:
		
		mydict[myID] = 1

################## record values into a dictionary

genefamilydict = defaultdict(dict)


for item in mydict:
	genefamily = item.split('|')[2]

	if item in keeplist:

		if mydict[item] in genefamilydict[genefamily]:
			genefamilydict[genefamily][mydict[item]] += 1
		else:
			genefamilydict[genefamily][mydict[item]] = 1

out = open('num_exons_per_family', 'w')
out2 = open('majority_num_exons.reference', 'w')

for thing in sorted(genefamilydict):
	out2.write(thing + '\t' + str(max(genefamilydict[thing].iteritems(), key=operator.itemgetter(1))[0]) + '\n')

	for number in sorted(genefamilydict[thing]):
		myout = '\t'.join([thing, str(number)+ ' segments', str(genefamilydict[thing][number])]) + '\n'*(number)
		myout2 = '\t'.join([thing, str(number) + ' segments', str(genefamilydict[thing][number])]) + '\n'
		if number == 1:
			out.write(myout2)
		else:
			out.write(myout)










