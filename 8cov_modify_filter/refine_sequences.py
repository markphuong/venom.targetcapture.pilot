import os
import sys
import numpy
from collections import defaultdict

##################### alternative alleles dictionary

altdict =defaultdict(dict)

myalternatives = open(sys.argv[1] + '_alternative_alleles', 'r')

for line in myalternatives:
	info = line.strip().split('\t')

	if info[0] in altdict.keys() and info[1] in altdict[info[0]].keys():

		altdict[info[0]][info[1]].append([int(info[2]), info[3], info[4]])
	else:
		altdict[info[0]][info[1]] = [ [int(info[2]), info[3], info[4]] ]
		


################################



myfasta = open(sys.argv[1] + '_definedseqs.fa', 'r')
out = open(sys.argv[1] + '_definedseqs_v2.fa','w')

fastadict = dict()


ID = sys.argv[1]

for line in myfasta:
	if ">" in line and "|0|0|" in line:
		continue
	elif ">" in line:

		header = line.strip()[1:]
		
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

for thing in fastadict:
	out.write('>' + thing + '\n')
	out.write(fastadict[thing] + '\n')

out.close()
