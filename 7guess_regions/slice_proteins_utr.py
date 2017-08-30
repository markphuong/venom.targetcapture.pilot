import os
import sys
from collections import defaultdict
from Bio.Seq import translate
from Bio.Seq import reverse_complement
from Bio import SearchIO


fastadict = dict()

myfasta = open('all_with_utrs.fa', 'r') #>Ar_B1_3|arenatus|B1|325.89298893_90_1|117|387|Ar_B1_3


for line in myfasta:
	if ">" in line: 
		fastadict[line.strip()[1:]] = next(myfasta).strip()


mybed = open('all_utr_annotated', 'r')
#mybed = open('test_annotated', 'r')

out = open('venom_proteins_sliced_utr.fa', 'w')


previous = 0
mylength = 0
for line in mybed:
	info = line.strip().split('\t')

	start = int(info[1])
	end = int(info[2])

	realstart = int(info[0].split('|')[-3])
	realend = int(info[0].split('|')[-2])



	exon = info[5]
	pieces = info[6]

	if exon == 'exon1':
		start = realstart
		print start
	if exon.replace('exon','') == pieces.replace('pieces', ''):
		end = realend




	if previous == info[0]:
		mylength = mylength
	else:
		mylength=0

	remainder = mylength%3

	previous = info[0]


	out.write('>' + info[0].split('|')[0] + '_utr' + '|' + '|'.join(info[0].split('|')[1:-3]) +'|'+ '|'.join(info[1:-1])+ '\n')
	out.write(translate('N'*remainder + fastadict[info[0]][start:end]).replace('X','') + '\n')

	mylength = mylength + end-start
	print mylength












