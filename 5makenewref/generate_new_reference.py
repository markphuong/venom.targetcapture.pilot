import os
import sys
from Bio.Seq import reverse_complement

###############################
myutr = open(sys.argv[2] + '_venom_genes_sliced.fa', 'r')

utrdict = dict()

for line in myutr:
	if ">" in line:
		utrdict[line.strip()[1:]] = next(myutr).strip()



####################################################################### load into dictionary all the possible assembled contigs


contigdict = dict()


mycontigs = open(sys.argv[1] + '_venom_contigs_reassembled.fa.NI.subset', 'r')

for line in mycontigs:
	if ">" in line:
		contigdict[line.strip().split(' ')[0][1:]] = next(mycontigs).strip()


#################################################### open the sliced genes, and blast them to the assembled venom contigs. take the best hit, and annotate it with where the identified exon is
################################################### and write out the entire sequence, so that you have a file now with venom gene exons with the proper annotations of exon number, and where the exon is


blastout = open(sys.argv[1] + '.filtered_reference.goodhits' ,'w')
seqout = open('mynewreference.fa' ,'a')
#seqout = open('mynewreference.fa_test' ,'w')

myblast = open(sys.argv[1] + '.venom_exon_slicing.blastoutput', 'r')
#myblast = open('test', 'r')

alreadyseen = []
contigseen = []
myfail = open('failed_generate_new_ref.fail', 'a')

for line in myblast:
	info = line.strip().split('\t')

	if 'didnotblast' in line:
		continue

	elif info[0] in alreadyseen:
		continue
	else:
		alreadyseen.append(info[0])
		if info[1] in contigseen:
			continue
		else:
			contigseen.append(info[1])

			blastout.write(line)

			header = info[0].split('|')

			genefamily = header[2]
			species = header[1]
			exon = header[-2]
			pieces = header[-1]
			gene = header[0]



			
			if int(info[8]) > int(info[9]):
				myoutseq = reverse_complement(contigdict[info[1]])
				start = len(contigdict[info[1]]) - int(info[8]) 
				end = len(contigdict[info[1]]) - int(info[9]) + 1

			else:
				myoutseq = contigdict[info[1]]
				start = int(info[8]) - 1
				end = int(info[9])

			codingstart = int(header[4])
			codingend = int(header[5])

			alignstart = int(info[6]) - 1
			alignend = int(info[7])
############ for utrs, had to modify start/end positions because I included sequences with the utr regions so that the sequence would be long enough to blast. I want the coordinates in the headers to only contain exon information

			if codingend - codingstart < 3:
				myfail.write(line)
				continue
			elif 'utr' in line:
				gene = gene + '_utr'

				myrange1 = range(codingstart, codingend)
				myrange2 = range(alignstart-1,alignend)
				if float(len(list(set(myrange1).intersection(myrange2))))/float(len(myrange1)) < 0.90:
					myfail.write(line.strip() + '\t95%\n')
					continue


				elif exon == 'exon1':


#					while (end - start) > (codingend-codingstart):
#						start = start + 1
					mynewstart = start + (codingstart - alignstart)
					mynewend = end - (codingend-alignend)

					#if there is an indel, just search for the coding region in the sequence and designate start/stop boundaries
					if int(info[5]) > 0:
						mycoding = utrdict[info[0]][codingstart:codingend]
						if mycoding in myoutseq:
							myfail.write(line.strip() + '\t' +str(mynewstart) + '\t' + str(mynewend))
							mynewstart = myoutseq.index(mycoding)
							mynewend = mynewstart + len(mycoding)
							myfail.write('\t' + str(mynewstart) + '\t' + str(mynewend) + '\n')

						else:
							mynewstart = mynewstart
							mynewend = mynewend
					if mynewend-mynewstart < 3:
						continue
						

					seqout.write('>' + '|'.join([info[1], gene, species, genefamily, exon, pieces, str(mynewstart), str(mynewend)]) +'\n')
					seqout.write(myoutseq + '\n')	
				elif exon.replace('exon','') == pieces.replace('pieces', ''):
#					while (end-start) > (codingend-codingstart):
#						end  = end-1
#					mynewstart = start + (alignstart - codingstart)
					mynewstart = start + (alignstart - codingstart)
					mynewend = end - (alignend-codingend)

					if int(info[5]) > 0:
						mycoding = utrdict[info[0]][codingstart:codingend]

						### did this manually because there was only one case where the solution to fixing the boundary wasn't applicable
						if 'Im_P_12' in line:
							mynewstart = 90
							mynewend = 95
						elif mycoding in myoutseq:
							myfail.write(line.strip() + '\t' +str(mynewstart) + '\t' + str(mynewend))
							mynewstart = myoutseq.index(mycoding)
							mynewend = mynewstart + len(mycoding)
							myfail.write('\t' + str(mynewstart) + '\t' + str(mynewend) + '\n')
						else:
							mynewstart = mynewstart
							mynewend = mynewend
					if mynewend-mynewstart < 3:
						continue
					
					seqout.write('>' + '|'.join([info[1], gene, species, genefamily, exon, pieces, str(mynewstart), str(mynewend)]) +'\n')
					seqout.write(myoutseq + '\n')	
#					print line

				else:
					continue						


			else:
				seqout.write('>' + '|'.join([info[1], gene, species, genefamily, exon, pieces, str(start), str(end)]) +'\n')
				seqout.write(myoutseq + '\n')














