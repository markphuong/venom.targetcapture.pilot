import os
import sys
from collections import defaultdict

mymap = open('species_name_mapping', 'r')

thekeys = []

############### loop through all samples, count number of venom genes per gene family

resultsdict = defaultdict(dict)
for line in mymap:
	info = line.strip().split('\t')

	ID = info[0]
	species = info[1]


	myfasta = open(ID + '_venom_analyzethese.fa', 'r')


	for line in myfasta:
		if ">" in line:
			info = line.strip().split('|')



			thekey = info[1] + '_' + info[-1]
			thekeys.append(thekey)

			if species in resultsdict and thekey in resultsdict[species]:
				resultsdict[species][thekey] += 1
			else:
				resultsdict[species][thekey] = 1

	myfasta.close()


#### table for supplementary
out = open('conotoxin_diversity_by_gf_exon_after_filtering.stats', 'w')

thekeys = list(set(thekeys))

myout = ['species']

for key in sorted(thekeys):
	myout.append(key.split('_')[0])

out.write('\t'.join(myout)+'\n')

myout = ['species']

for key in sorted(thekeys):
	myout.append(key.split('_')[1])

out.write('\t'.join(myout)+'\n')


for thing in resultsdict:
	myout = [thing]
	for key in sorted(thekeys):
		if key in resultsdict[thing]:
			myout.append(str(resultsdict[thing][key]))
		else:
			myout.append('0')
	out.write('\t'.join(myout) + '\n')


############### input for R

out2 = open('diversity_stats_for_r.stats', 'w')

thekeys = list(set(thekeys))

myout = ['species'] #write out headers

for key in sorted(thekeys):
	key=' '.join(key.split('|')[0:2])

	myout.append(key)



out2.write('\t'.join(myout)+'\n')

# write out values per species, in specific order

for thing in resultsdict:
	myout = [thing]
	for key in sorted(thekeys):
		if key in resultsdict[thing]:
			myout.append(str(resultsdict[thing][key]))
		else:
			myout.append('0')
	out2.write('\t'.join(myout) + '\n')







