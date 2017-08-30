import os
import sys


myclstr = open(sys.argv[1],'r')


clusterdict = dict()


for line in myclstr:
	if 'Cluster' in line:
		key = line.strip().replace(' ', '').replace('>', '')

	else:
		if key in clusterdict:
			clusterdict[key].append(line.strip().split('>')[1].split('...')[0])
		else:
			clusterdict[key] = [line.strip().split('>')[1].split('...')[0]]

out = open('mapfile.pdist.venom', 'a')

for key in clusterdict:
	alreadyseen = []
	
	
	for ID1 in clusterdict[key]:
		for ID2 in clusterdict[key]:
			if ID1 == ID2:
				continue
			elif ID1 + '---' + ID2 in alreadyseen or ID2 + '---' + ID1 in alreadyseen:
				continue
			else:
				alreadyseen.append(ID1 + '---' + ID2)
				

				out.write('\t'.join([ID1, ID2, sys.argv[2]]) + '\n')















