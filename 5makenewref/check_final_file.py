import os
import sys
from Bio.Seq import translate

myfasta = open('index8_venom_utrs_reassembled.fa.NI.subset.CO.annotated', 'r')

for line in myfasta:
	if ">" in line:

		header = line.strip().split('|')
		seq = translate(next(myfasta).strip()[int(header[-2]):int(header[-1])])

#		print line
		if seq[0] == 'M' and seq[-1] == '*':
			if not '*' in seq:
				
		else:
			print line
			print seq

		
