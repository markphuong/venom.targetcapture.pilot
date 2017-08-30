import os
import sys
import numpy
from collections import defaultdict



############################# if the haplotype file exists, store the phased haplotype information in a dictionary. only consider heterozygotes that are within the coding region
ID = sys.argv[1]

hapfile = open(ID + '_output_haplotype_file', 'r')

hapdict = defaultdict(dict)

for line in hapfile:
	if 'BLOCK' in line or '********' in line or 'didnotexonerate' in line:
		continue
	else:
		info = line.strip().split('\t')

		header = info[3]
		start = int(header.split('|')[-3])
		end = int(header.split('|')[-2])

		################# have to do -1 because off by one on VCF file; it starts counting by 1
		if int(info[4]) - 1 >= start and int(info[4])-1 <= end:
			hapdict[header][int(info[4])-1] = [info[5], info[6]]
		else:
			continue
		



myfasta = open(sys.argv[2], 'r')
out = open(ID + '_haplotypes.fa', 'w')

####################################### write out all haplotypes, but only the coding regions
for line in myfasta:
	if '>' in line:
		header = line.strip()[1:]
		start = int(header.split('|')[-3])
		end = int(header.split('|')[-2])
		seq = next(myfasta).strip()


####################################### if the haplotypes exist, write out both sequences
		if header in hapdict.keys():
			seq1 = list(seq)
			seq2 = list(seq)
			for item in hapdict[header]:
				seq1[item] = hapdict[header][item][0]
				seq2[item] = hapdict[header][item][1]
			out.write(line.strip() +'|hap1' + '\n')
			out.write(''.join(seq1[start:end])+ '\n')
			out.write(line.strip() +'|hap2' + '\n')
			out.write(''.join(seq2[start:end])+ '\n')									

################################### else, just write out the single copy
		else:
			out.write(line.strip() +'|onecopy' + '\n')
			out.write(seq[start:end]+ '\n')
	else:
		continue






