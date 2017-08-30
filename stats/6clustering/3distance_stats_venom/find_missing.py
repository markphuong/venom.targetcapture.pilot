import os
import sys


mymap = open('mapfile.pdist.venom', 'r')

mylist = []

for line in mymap:
	mylist.append(line.strip())


myvenom = open('venom.datapoint', 'r')

mylist2 = []

for line in myvenom:
	info = '\t'.join(line.strip().split('\t')[0:3])

	mylist2.append(info)

out = open('map_notdoneyet', 'w')

for item in set(mylist).difference(mylist2):
	out.write(item + '\n')