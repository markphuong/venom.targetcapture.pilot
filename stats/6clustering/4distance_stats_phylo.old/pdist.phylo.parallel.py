import os
import sys
from collections import defaultdict
import multiprocessing
import argparse


def get_args(): #arguments needed to give to this script
        parser = argparse.ArgumentParser(description="run novoalign")

        #forces required argument to let it run
        required = parser.add_argument_group("required arguments")
        required.add_argument("--map", help="textfile with samples to run and what fasta file to match it to", required=True) #A map file with the sample ID and the fasta file it goes to

        return parser.parse_args()


def pdist(seq1, seq2):
	"""Sequences must be strings, have the same length, and be aligned"""
	num = 0
	diff = 0
	for i, nucleotide in enumerate(seq1):
		couple = [nucleotide, seq2[i]]
		if couple[0] == "-" or couple[0] == 'N':
			continue
		elif couple[1] == "-" or couple[1] == 'N':
			continue
		elif couple[0] == couple[1]:
			num += 1
		elif not couple[0] == couple[1]:
			num += 1
                        diff += 1
	if num == 0:
		return ['NA', '0']
	else:

		pdist = float(diff)/float(num)
		return [pdist,num]




def align(element):
	myfasta = open('all_cut_up_exons_plus_introns.fa', 'r')

	fastadict = defaultdict(dict)

	for line in myfasta:
		if ">" in line:
			info = line.strip()[1:].split('|')

			species = info[0]

			locus = '|'.join(info[4:])

			start = int(info[2])
			end = int(info[3])

			fastadict[species][locus] = [next(myfasta).strip(), start, end]

	myfasta.close()

	ID1 = element[0]
	ID2 = element[1]
	locus = element[2]




	myuniqueID = ID1 + '_' + ID2 + '_' + locus.replace('|','_')

	out = open(myuniqueID + '.pdist.datapoint', 'w')


	tempfasta = open(myuniqueID + '_tempfasta', 'w')

	tempfasta.write('>' + ID1+'\n')
	tempfasta.write(fastadict[ID1][locus][0] + '\n')
	tempfasta.write('>' + ID2 + '\n')
	tempfasta.write(fastadict[ID2][locus][0] + '\n')
	tempfasta.close()

####### run mafft and format file for reinput into this script

	os.system('mafft --preservecase --adjustdirection --auto ' + myuniqueID + '_tempfasta > ' + myuniqueID + '_tempfasta.aligned')
	os.system('python makesomethingNotInterleaved.py ' + myuniqueID + '_tempfasta.aligned ' + myuniqueID + '_tempfasta.aligned.NI')

			
######################## open aligned and find start end for coding regions..

	myaligned = open(myuniqueID + '_tempfasta.aligned.NI', 'r')

	starts = []
	ends = []

	seq1 = ''
	seq2 = ''

	for line in myaligned:
		if ">" in line:

			myseq = next(myaligned).strip()

		if line.strip()[1:].replace('_R_','') == ID1:
			seq1 = myseq
			start = fastadict[ID1][locus][1]
			end = fastadict[ID1][locus][2]
			if '_R_' in line:
				start = len(myseq.replace('-','')) - fastadict[ID1][locus][2]
				end = len(myseq.replace('-','')) - fastadict[ID1][locus][1]
		else:
			seq2 = myseq

			start = fastadict[ID2][locus][1]
			end = fastadict[ID2][locus][2]
			if '_R_' in line:
				start = len(myseq.replace('-','')) - fastadict[ID2][locus][2]
				end = len(myseq.replace('-','')) - fastadict[ID2][locus][1]


	
		myseq = list(myseq)	

		counter = 0

		position = 0
		myrealstart = 0
		myrealend = 0

		while counter < len(myseq):
			if position == start:
				myrealstart = counter


			if myseq[counter] == '-':
				counter += 1
			else:
				counter += 1
				position += 1
			if position == end:
				myrealend = counter
		starts.append(myrealstart)
		ends.append(myrealend)

	myaligned.close()

	mystart = min(starts)
	myend = max(ends)
	print starts
	print ends
	print mystart
	print myend
	seq1coding = seq1[mystart:myend]
	seq2coding = seq2[mystart:myend]
	seq1noncoding = seq1[0:mystart] + seq1[myend:]
	seq2noncoding = seq2[0:mystart] + seq2[myend:]

	print seq1coding
	print seq2coding
	print seq1noncoding
	print seq2noncoding

	pdistcoding = pdist(seq1coding,seq2coding)
	pdistnoncoding = pdist(seq1noncoding, seq2noncoding)

	out.write('\t'.join([ID1, str(fastadict[ID1][locus][1]),str(fastadict[ID1][locus][2]), ID2, str(fastadict[ID2][locus][1]), str(fastadict[ID2][locus][2]), locus, str(pdistcoding[0]), str(pdistcoding[1]), str(pdistnoncoding[0]), str(pdistnoncoding[1])]) + '\n')

	out.close()






mylist = []
def main():



        args = get_args()

        #Make a list of lists, each list within the list will have the first and second elements of the map file that are separated by a tab

        with open(args.map) as rfile:
                for line in rfile:
                        line = line.strip().split('\t')
#			align(line)
                        mylist.append(line)

        pool = multiprocessing.Pool(3)
        pool.map(align, mylist)#run the function with the arguments

if __name__ == "__main__": #run main over multiple processors
        main()
































		


























