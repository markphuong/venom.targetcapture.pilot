import os
import sys
from collections import defaultdict


########### get the number of sequences targetted per gene family per species from 'venom_reference.fa'


genefamilylist = []

targetdict = defaultdict(dict)
myfasta = open('venom_reference.fa', 'r')

for line in myfasta:
	if ">" in line:
		info = line.strip().split('|')
		

		species = info[1]
		genefamily = info[2]


		genefamilylist.append(genefamily)

		if species in targetdict.keys() and genefamily in targetdict[species].keys():
			targetdict[species][genefamily] += 1
		else:
			targetdict[species][genefamily] = 1
myfasta.close()






################################ open venom bed file and get a dictionary of lengths of the blastable regions
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


####################### flip through fasta file. a sequence has been recovered if it exists in the bed file for more than 80% of the sequence
sequenceddict = defaultdict(dict)
totaldict = defaultdict(dict)

seqtotdict = dict()
totdict = dict()

myfasta = open('all_extractedseq_renamed.fa', 'r')

failed = open('did_not_sequence','w')

for line in myfasta:
	if ">" in line:
		info = line.strip().split('|')

		species = info[1]

		genefamily = info[2]

		if genefamily in totdict.keys():
			what = 'cool'
		else:
			seqtotdict[genefamily] = 0
			totdict[genefamily] = 0


		seq = next(myfasta).strip()

		if species in totaldict.keys() and genefamily in totaldict[species].keys():
			totaldict[species][genefamily] += 1
			totdict[genefamily] += 1
		else:
			totaldict[species][genefamily] = 1
			totdict[genefamily] += 1

		if line.strip()[1:] in counterdict:		
			if float(counterdict[line.strip()[1:]])/float(len(seq)) > .8:


				if species in sequenceddict.keys() and genefamily in sequenceddict[species].keys():
					sequenceddict[species][genefamily] += 1
					seqtotdict[genefamily] +=1
				else:
					sequenceddict[species][genefamily] = 1
					seqtotdict[genefamily] +=1
			else:
				failed.write(line)
		
		else:
			failed.write(line)


########### output the file table

out = open('conus_venom_captured.table', 'w')

out2 = open('conus_venom_captured_percentages', 'w')

out.write('species' + '\t' + '\t'.join(sorted(list(set(genefamilylist)))) + '\n')
out2.write('species' + '\t' + '\t'.join(sorted(list(set(genefamilylist)))) + '\n')



for species in sorted(totaldict):

	myoutput = []
	myoutput2 = []

	myoutput.append(species)
	myoutput2.append(species)


	for genefamily in sorted(set(genefamilylist)):

		if genefamily in totaldict[species]:

			if genefamily in sequenceddict[species]:
				sequenced = sequenceddict[species][genefamily]
			else:
				sequenced = 0

			if genefamily in targetdict[species]:
				targeted = targetdict[species][genefamily]
			else:
				targeted = 0



			myoutput.append(str(targeted) + ', ' +str(sequenced) + '/' + str(totaldict[species][genefamily]))
			myoutput2.append(str(float(sequenced)/float(totaldict[species][genefamily])))
		else:
			myoutput.append('-')
			myoutput2.append('-')


	




	out.write('\t'.join(myoutput) + '\n')
	out2.write('\t'.join(myoutput2) + '\n')

myoutput3 = ['cap success']

for genefamily in sorted(set(genefamilylist)):
	if genefamily in seqtotdict:
		print genefamily, seqtotdict[genefamily], totdict[genefamily]
		myoutput3.append(str(float(seqtotdict[genefamily])/float(totdict[genefamily])))
	else:
		myoutput3.append('0.00')

out.write('\t'.join(myoutput3) + '\n')			


		













