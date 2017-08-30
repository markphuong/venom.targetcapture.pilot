import os
import sys

myfasta = open(sys.argv[1], 'r')

fastadict = dict()

for line in myfasta:
	if ">" in line:
		fastadict[line.strip()[1:]] = next(myfasta).strip()

#print fastadict


myblast = open(sys.argv[2], 'r')



blastdict = dict()

for line in myblast:
	info = line.strip().split('\t')

	if int(info[8]) > int(info[9]):
		start = int(info[9]) - 1
		end = int(info[8]) 
	else:
		start = int(info[8]) - 1
		end = int(info[9])

	if float(len(range(start,end)))/float(len(fastadict[info[1]])) > 0.7:
		if info[0] in blastdict:
		
			blastdict[info[0]].append(info[1])
		else:
			blastdict[info[0]] = [info[1]]

maxvalue = 0

for thing in blastdict:
	maxvalue = max(maxvalue,len(list(set(blastdict[thing])))) 

mykey = ''

for thing in blastdict:
	if maxvalue == len(list(set(blastdict[thing]))):
		mykey = thing
		specieslist = []
		for ID in blastdict[thing]:
			specieslist.append(ID.split('|')[-2])

out3 = open(sys.argv[3] + '.stats', 'w')

out3.write('\t'.join([sys.argv[3], str(len(list(set(specieslist)))), str(maxvalue), str(len(blastdict))]))



out = open(sys.argv[3] + '.align.these.first', 'w')

for ID in set(blastdict[mykey]):
	out.write('>' + ID + '\n')
	out.write(fastadict[ID] + '\n')

out2 = open(sys.argv[3] + '.add.these.later', 'w')

for ID in fastadict:
	if ID in blastdict[mykey]:
		continue
	else:
		out2.write('>' + ID + '\n')
		out2.write(fastadict[ID] + '\n')



















 		
