import os
import sys


myfasta = open(sys.argv[1], 'r')

fastaIDs = []

for line in myfasta:
	if ">" in line:
		fastaIDs.append(line.strip()[1:])

myfasta2 = open(sys.argv[2], 'r')


for line in myfasta2:
	if ">" in line:
		if '|'.join(line.strip()[1:].split('|')[:-1]) in fastaIDs:
			fastaIDs.remove('|'.join(line.strip()[1:].split('|')[:-1]))

out = open(sys.argv[3], 'w')

for item in fastaIDs:
	out.write(item + '\n')