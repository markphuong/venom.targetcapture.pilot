import os
import sys
from Bio.Seq import reverse_complement


############ create dictionary of all your venom genes from phuong et al 2016
myfasta = open(sys.argv[2]+'_with_utrs.fa', 'r')

fastadict = dict()

for line in myfasta:
	if ">" in line:
		fastadict[line.strip()[1:]] = next(myfasta).strip()



myfasta.close()


#############################################################  write out the sliced exons into a new file based on venombed file

mybed = open(sys.argv[2] + '_venombed_utr_annotated', 'r')

out = open(sys.argv[2] + '_venom_genes_sliced.fa', 'a')

for line in mybed:

	info = line.strip().split('\t')

	newID = '|'.join(info[0].split('|')[:-3])+'_containsutr'

	start = int(info[1])
	end = int(info[2])

	codestart = int(info[0].split('|')[4])
	codeend = int(info[0].split('|')[5])

	myrange1 = range(start, end)
	myrange2 = range(codestart,codeend)

	if 'didnotblast' in line:
		continue
	elif len(list(set(myrange1).intersection(myrange2))) == len(myrange1):

		out.write('>' + newID + '|' + '|'.join(info[1:]) + '\n')
		out.write(fastadict[info[0]][start:end] + '\n')
	elif start < codestart:

		mycoding = fastadict[info[0]][codestart:end]
		mywrittenseq = fastadict[info[0]][start:end]

		mynewstart = mywrittenseq.index(mycoding)
		mynewend = mynewstart + len(mycoding)

######### did new mynewstart and mynewend because wanted to know exactly where the coding region was in the sequence once I sliced it up


		out.write('>' + newID + '|' + str(mynewstart) + '|' + str(mynewend) + '|' + '|'.join(info[3:]) + '\n')
		out.write(fastadict[info[0]][start:end] + '\n')

	else:
		mycoding = fastadict[info[0]][start:codeend]
		mywrittenseq = fastadict[info[0]][start:end]

		mynewstart = mywrittenseq.index(mycoding)
		mynewend = mynewstart + len(mycoding)

		out.write('>' + newID + '|' + str(mynewstart) + '|' + str(mynewend) + '|' + '|'.join(info[3:]) + '\n')
		out.write(fastadict[info[0]][start:end] + '\n')









out.close()