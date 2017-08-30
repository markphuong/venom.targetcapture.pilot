import os
import sys
from Bio.Seq import reverse_complement

myfasta = open(sys.argv[1], 'r')

fastadict = dict()

for line in myfasta:
	if ">" in line:
		fastadict[line.strip().split(' ')[0][1:]] = next(myfasta).strip()


myblast = open(sys.argv[2], 'r')

alreadyseen = []

out = open(sys.argv[3], 'w')
blastgood = open(sys.argv[4], 'w')
blastfail = open(sys.argv[5], 'w')

for line in myblast:
	info = line.strip().split('\t')
	if info[0] in alreadyseen:
		continue
	else:
		if int(info[8]) > int(info[9]):
			outseq = reverse_complement(fastadict[info[0]])
			start = int(info[9]) - 1
			end = int(info[8])
		else:
			outseq = fastadict[info[0]]
			start = int(info[8]) - 1
			end = int(info[9])

		exonstart = int(info[1].split('|')[-2])
		exonend = int(info[1].split('|')[-1])

		if start <= exonstart and end >= exonend:
			out.write('>' + info[0] + '\n')
			out.write(outseq + '\n')
			blastgood.write(line)
		else:
			blastfail.write(line)

		alreadyseen.append(info[0])

	