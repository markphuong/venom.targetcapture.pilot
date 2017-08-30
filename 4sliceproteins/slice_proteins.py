import os
import sys
from collections import defaultdict
from Bio.Seq import translate
from Bio.Seq import reverse_complement
from Bio import SearchIO


fastadict = dict()

myfasta = open('all_extractedseq_renamed.fa', 'r')

for line in myfasta:
	if ">" in line: 
		fastadict[line.strip()[1:]] = next(myfasta).strip()


mybed = open('venombed', 'r')
#mybed = open('mytestbed', 'r')

out = open('venom_proteins_sliced.fa', 'w')

for line in mybed:
	info = line.strip().split('\t')

	start = int(info[1])
	end = int(info[2])

	remainder = start%3



	out.write('>' + '|'.join(info)+ '\n')
	out.write(translate('N'*remainder + fastadict[info[0]][start:end]).replace('X','') + '\n')















