import os
import sys


myref = open('venom_reference.fa', 'r')

mygenelist = []

for line in myref:
	if ">" in line:
		info = line.strip().split('|')
		mygenelist.append(info[2])

myref.close()

mygenelist = sorted(list(set(mygenelist)))
print 'venom_reference'
print mygenelist
print len(mygenelist)


### wrote this bit of code to figure out which gene families were not targetted
transcriptome = open('transcriptome.genefamilies', 'r')

for line in transcriptome:
	info = line.strip().split('\t')

	for thing in info:
		if thing in mygenelist:
			continue
		else:
			print thing

myref = open('all_stats_venombed_annotated_v3', 'r')

mygenelist = []

for line in myref:
	info = line.strip().split('\t')[0].split('|')
	mygenelist.append(info[2])


mygenelist = sorted(list(set(mygenelist)))
print 'recovered'
print mygenelist
print len(mygenelist)

myref.close()


