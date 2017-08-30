import os
import sys
from Bio.Seq import reverse_complement


############ create dictionary of all your venom genes from phuong et al 2016
myfasta = open('all_extractedseq_renamed.fa', 'r')

fastadict = dict()

for line in myfasta:
	if ">" in line:
		fastadict[line.strip()[1:]] = next(myfasta).strip()



myfasta.close()


#############################################################  write out the sliced exons into a new file based on venombed file

mybed = open(sys.argv[2] + '_stats_venombed_annotated', 'r')

out = open(sys.argv[2] + '_stats_venom_genes_sliced.fa', 'w')

for line in mybed:

	info = line.strip().split('\t')

	out.write('>' + '|'.join(info) + '\n')
	out.write(fastadict[info[0]][int(info[1]):int(info[2])] + '\n')

out.close()