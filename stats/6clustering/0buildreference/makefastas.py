import os
import sys

mapfile = open('mapfile', 'r')


for line in mapfile:

	info = line.strip().split('\t')
	species = info[1]
	identifier = info[0]

	fastadict = dict()

	myfasta = open(identifier+ '_definedseqs_v6.fa', 'r')

	for line in myfasta:
		if ">" in line:
			fastadict[line.strip()[1:]] = next(myfasta).strip()



	myfasta.close()



	myfile = open(species +'.my.region.assignments.info', 'r')

	assignments = dict()

	for line in myfile:
		info = line.strip().split('\t')

		if info[-1] in assignments:
			assignments[info[-1]].append(info[-2])
		else:
			assignments[info[-1]] = [info[-2]]

	myfile.close()

###### ignored sequences that had multiple assignments

	out = open(identifier + '.regions.identified.fa', 'w')

	seenlist = []

	for ID in assignments:
		myregion = list(set(assignments[ID]))


		if ID == 'FAILED':
			continue
		elif len(myregion) == 1 and not ID in seenlist:
			out.write(">" + ID + '|' + identifier + '|' + species+ '|' + myregion[0] + '\n')
			out.write(fastadict[ID + '|' + identifier + '|' + species] + '\n')

			seenlist.append(ID)

		else:
			continue
	out.close()



















