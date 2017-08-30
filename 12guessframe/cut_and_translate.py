import os
import sys
from Bio.Seq import translate


myfasta = open(sys.argv[1], 'r')

guessed = open(sys.argv[3], 'w')

out = open(sys.argv[2], 'w')

ID = sys.argv[1].split('_')[0]

for line in myfasta:
	if ">" in line:
		if 'guessed' in line:
			guessed.write(line.strip()+'|' + ID + '\n')
			guessed.write(next(myfasta))
		else:
			info = line.strip().split('|')
			start = int(info[4])
			end = int(info[5])

			seq = translate(next(myfasta).strip()[start:end])

			out.write(line.strip()+'|' + ID + '\n')
			out.write(seq + '\n')