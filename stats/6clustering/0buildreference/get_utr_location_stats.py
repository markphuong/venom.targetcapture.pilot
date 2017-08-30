import os
import sys
from collections import defaultdict

observeddict = defaultdict(dict)
totaldict = defaultdict(dict)

myfile = open('all_my_utr_info', 'r')

for line in myfile:
	info = line.strip().split('\t')

	genefamily = info[0].split('|')[2] + '|' + info[2]
	prime = info[-1]
	utr = info[-3]

	if 'didnotlocallyalignfully' in line:
		continue
	else:
		if genefamily in totaldict and prime in totaldict[genefamily]:
			totaldict[genefamily][prime] += 1
			if utr == 'yes':
				observeddict[genefamily][prime] += 1
			else:
				observeddict[genefamily][prime] += 0
		else:
			totaldict[genefamily][prime] = 1
			if utr == 'yes':
				observeddict[genefamily][prime] = 1
			else:
				observeddict[genefamily][prime] = 0



out = open('utr_locations', 'w')
out2 = open('utr_locations_add_to_region', 'w')	
 
for genefamily in sorted(totaldict):
	for prime in sorted(totaldict[genefamily]):
		out.write('\t'.join([genefamily.split('|')[0],genefamily.split('|')[1], prime, str(observeddict[genefamily][prime]), str(totaldict[genefamily][prime]), str(float(observeddict[genefamily][prime])/float(totaldict[genefamily][prime]))]) + '\n')

		if '1pieces' in genefamily:
			if prime == '3prime':
				out2.write('\t'.join([genefamily.split('|')[0],genefamily.split('|')[1], str(float(observeddict[genefamily]['3prime'])/float(totaldict[genefamily]['3prime'])), str(float(observeddict[genefamily]['5prime'])/float(totaldict[genefamily]['5prime']))]) + '\n')


		elif prime == '3prime':
			out2.write('\t'.join([genefamily.split('|')[0],genefamily.split('|')[1], str(float(observeddict[genefamily][prime])/float(totaldict[genefamily][prime])), '-']) + '\n'*(int(genefamily.split('|')[1].replace('pieces',''))-1))

		else:		
			out2.write('\t'.join([genefamily.split('|')[0],genefamily.split('|')[1], '-', str(float(observeddict[genefamily][prime])/float(totaldict[genefamily][prime]))]) + '\n')











