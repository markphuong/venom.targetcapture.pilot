import os
import sys

myfile = open('all_extractedseq_renamed.fa', 'r')


alreadyseen = []

for line in myfile:
	if ">" in line:
		info = line.strip()[1:].split('|')
		if info[0] in alreadyseen:
			print line
		else:
			alreadyseen.append(info[0])		