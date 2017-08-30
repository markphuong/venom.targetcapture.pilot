import os
import sys
import numpy
from collections import defaultdict

##################### alternative alleles dictionary

altdict =defaultdict(dict)

myalternatives = open(sys.argv[1] + '_alternative_alleles_dir9', 'r')

for line in myalternatives:
	info = line.strip().split('\t')

	if info[0] in altdict.keys() and info[1] in altdict[info[0]].keys():

		altdict[info[0]][info[1]].append([int(info[2]), info[3], info[4]])
	else:
		altdict[info[0]][info[1]] = [ [int(info[2]), info[3], info[4]] ]
		





####################### load dictionary of coverage

ID = sys.argv[1]

mycov = open(ID + '_dir9.cov', 'r')

covdict = dict()

for line in mycov:
	info = line.strip().split('######')

	covlist = info[1][1:-1].split(', ')

	covlist = [int(item) for item in covlist]
	covdict[info[0]] = covlist
	

####################### load dictionary of sequences
myfasta = open(sys.argv[1] + '_definedseqs_v2.fa', 'r')

fastadict = dict()
headerlist=[]

for line in myfasta:
	if ">" in line:

		header = line.strip()[1:]
		headerlist.append(header)
		seq = next(myfasta).strip()

		seq = list(seq)

		if header in altdict[ID]:
			for item in altdict[ID][header]:
				if ',' in item[1]:
					seq[item[0]-1] = 'N'
				elif item[2] == '1/1':
					seq[item[0]-1] = item[1]
				else:
					continue


		fastadict[header] = ''.join(seq)


myfasta.close()
################ some contigs may not show up in the VCF file, so you have to create lists of 0's and put them in your cov and het dictionaries

for item in set(headerlist):
	if item in covdict.keys():
		continue
	else:
		covdict[item] = [0]*4000

############################################################################




out = open(ID + '_definedseqs_v3.fa', 'w')
failed = open(ID  + '_failed_cov.fa', 'w')


for item in sorted(fastadict):

	header = item
	seq = fastadict[item]

	start = int(header.split('|')[-3])
	end = int(header.split('|')[-2])


	mysubset = covdict[header][start:end]

	if all(i >= 10 for i in mysubset):


		out.write('>'+ header +'\n')
		out.write(seq + '\n')
	else:
		failed.write('>' + header + '\n')
		failed.write(seq+'\n')
























