import os
import sys
from collections import defaultdict
import numpy
myfile = open("conus.prey.families.added.txt", 'r')



dbdict = dict() ###### store papers that have h values

myHdata = defaultdict(dict) ### store h values

dietdata = defaultdict(dict) ####### store all raw prey counts

specieslist = [] ### store species names

########## parse data

for line in myfile:
	info = line.strip().split('\t')

	if info[0] == 'species':
		what = 'what'
	else:
		specieslist.append(info[0])

	if 'dietary breadth' == info[1]:
		if info[0] in dbdict:
			dbdict[info[0]].append(info[-4] + '|' + info[-2] + '|' + info[-1])
			myHdata[info[0]][info[-4] + '|' + info[-2] + '|' + info[-1]] = info[2]
		else:
			dbdict[info[0]] = [info[-4] + '|' + info[-2] + '|' + info[-1]]
			myHdata[info[0]][info[-4] + '|' + info[-2] + '|' + info[-1]] = info[2]

	
	if 'diet specificity' == info[1]:
		if info[4] == 'NA':
			continue
		elif 'Nereid' in info[2] or 'Spionidae' in info[2] or 'Nereiidae' in info[2] or 'Capitellid' in info[2] or 'Syllid' in info[2] or 'Sabellarid' in info[2] or 'Maldanid' in info[2] or 'Terebellid' in info[2] or 'Maldanid' == info[2] or 'Terebellid uncini sp. 1' == info[2] or 'Terebellid uncini sp. 2' == info[2] or 'Capitellid' == info[2] or 'Nereid' == info[2] or 'Amphinomid?' == info[2] or 'Maldanidae sp.' == info[2] or 'spp.' in info[2] or 'Undetermined' in info[2] or 'unidentified' in info[2] or 'Unidentified' in info[2] or 'Other' in info[2] or 'NA' == info[3] or 'Unidentfied' in info[2]:
			continue
		elif info[0] in dietdata and info[-4] + '|' + info[-2] + '|' + info[-1] in dietdata[info[0]]:
			dietdata[info[0]][info[-4] + '|' + info[-2] + '|' + info[-1]].append(info[2] + '|' + info[3])
		else:
			dietdata[info[0]][info[-4] + '|' + info[-2] + '|' + info[-1]] = [info[2] + '|' + info[3]]

#################### write out information if observations are at least 5 prey items identified 


out = open('dietary.breadth.calculations', 'w')
preys = []
for species in sorted(dietdata):
	for paper in dietdata[species]:
		if species in dbdict and paper in dbdict[species]:
			continue
		else:
			totalobs = 0

			for value in dietdata[species][paper]:
				totalobs += int(value.split('|')[1])

################## calculate h index if at least 5 prey items discovered
			if totalobs >= 5:


				


				thesum = 0				
				for value in dietdata[species][paper]:
					preys.append(value.split('|')[0])
					mynum = float(value.split('|')[1])

					myp = mynum/float(totalobs)
					mylnp = numpy.log(mynum/float(totalobs))

					multiplied = myp * mylnp
					thesum += multiplied

					output = [species, 'thecalculations', value.split('|')[0], str(mynum), str(myp), str(mylnp), str(multiplied), paper.split('|')[0], paper.split('|')[1], paper.split('|')[2]]


					out.write('\t'.join(output) + '\n')
				output2 = [species, 'dietarybreadthvalue', str(thesum)]
				out.write('\t'.join(output2) + '\n')
				myHdata[species][paper] = thesum*-1



print sorted(set(preys))
#### helps me identify prey items I need to filter for
for item in sorted(set(preys)):
	if 'sp.' in item:
		print item


print myHdata

########## write out all the H values

hvalueout = open('all.hvalues.stats', 'w')
averagehvalues = open('average.h.values', 'w')


for species in sorted(set(specieslist)):

	averages = 0
	total = 0
	if species in myHdata:
		for paper in myHdata[species]:
			hvalueout.write('\t'.join([species,paper.split('|')[0], paper.split('|')[1], paper.split('|')[2], str(myHdata[species][paper])])+'\n')
			averages += float(myHdata[species][paper])
			total+= 1
		averagehvalues.write('\t'.join([species, str(averages/total)]) + '\n')		
	else:
		averagehvalues.write('\t'.join([species, 'NA']) + '\n')




#print dbdict
#print myHdata
#print dietdata