import os
import sys
from collections import defaultdict
from Bio.Seq import translate
from Bio.Seq import reverse_complement
from Bio import SearchIO
from operator import itemgetter

###### check for overlapping blast coordinates


def checkoverlap(a, b):
	overlap = max(0, min(a[1], b[1]) - max(a[0], b[0]))
        length1 = len(range(a[0],a[1]+1))

	length2 = len(range(b[0],b[1]+1))

	ratio1 = float(overlap)/length1
	ratio2 = float(overlap)/length2

	return max(ratio1, ratio2)



## load the fastafile, make it not interleaved, and make a blast database

variables = dict(
ref = sys.argv[2] + '_venom_contigs_reassembled.fa'
) #name your output


commands = """
python makesomethingNotInterleaved.py {ref} {ref}.NI
python chooseone.py {ref}.NI {ref}.NI.subset
makeblastdb -dbtype nucl -in {ref}.NI.subset
""".format(**variables)

cmd_list = commands.split("\n")
for cmd in cmd_list:
	os.system(cmd)


## create a dictionary of fasta IDs and sequences

fastadict = dict()

myfastafile = open(sys.argv[2] + '_venom_contigs_reassembled.fa.NI.subset', 'r')

for line in myfastafile:
	if ">" in line:
		fastadict[line.strip()[1:].split(' ')[0]] = next(myfastafile).strip()


###### for each protein identified from transcriptome work, blast it to the assembled exon capture data venom genes for that specific gene family, 
### and find the contigs that blast to the first and second exon/intron, then create a genomic sequence by combining the two contigs and
### run exnerate and get the exact cutting coordinates.

myprots = open(sys.argv[1] + '_extractedseq.fa', 'r') 

for line in myprots:
	if ">" in line:

		header = line.strip()[1:]

		seq = next(myprots)

		mytemp = open('myprot.fa', 'w')

		mytemp.write(line)
		mytemp.write(seq)

		mytemp.close()

########## do blast, 1 untranslated sequence to all venom contigs
		variables = dict(
		prot = 'myprot.fa',
		ref = sys.argv[2] + '_venom_contigs_reassembled.fa.NI.subset',
		sample = sys.argv[2]
		) #name your output

		commands = """
		blastn -query {prot} -db {ref} -outfmt 6 -out {sample}.mytempblast -evalue 1e-10 -word_size 11 -perc_identity 90
		""".format(**variables)

		cmd_list = commands.split("\n")
		for cmd in cmd_list:
			os.system(cmd)

		if os.path.getsize(sys.argv[2] + '.mytempblast') == 0:
			didnotblast = open(sys.argv[2] + '.didnotblast', 'a')
			didnotblast.write(header + '\n')
			didnotblast.close()
		else:


########## find first and second exon

			myblast = open(sys.argv[2] + '.mytempblast', 'r')


			keeplist = []

			cutcoords = open(sys.argv[1] + '_venomblastcoordfile', 'a')
			coordlist = []

			for line in myblast:
				info = line.strip().split('\t')
			
				if len(keeplist) == 0:
					keeplist.append([int(info[6]), int(info[7]), info[1], int(info[8]), int(info[9])])
					coordlist.append([int(info[6]),line])
				else:

					keepcontig = 'yes'
					for item in keeplist:
	
						a = [int(info[6]), int(info[7])]
						b = [item[0], item[1]]

						if checkoverlap(a,b) > .2:
							keepcontig = 'no'
						else:
							continue
					if keepcontig == 'yes':
						keeplist.append([int(info[6]), int(info[7]), info[1], int(info[8]), int(info[9])])
						coordlist.append([int(info[6]),line])
					else:
						continue
			myblast.close()


############# output blast coordinates in order
			for item in sorted(coordlist, key=itemgetter(0)):
				cutcoords.write(item[-1])
			cutcoords.close()			
			


			keeplist = sorted(keeplist, key=itemgetter(0))
#			print keeplist

##################### if the whole sequence is blasted, use exonerate to define exon boundaries, if not, used blast to define exon boundaries

			rangelist = []

			for item in keeplist:
				for i in range(item[0]-1,item[1]):
					rangelist.append(i)


			if len(seq.strip()) == len(list(set(rangelist))):

			
############ create a genome sequence for exonerate
				genomeseq = ''
	
				for myitem in sorted(keeplist):
					contigname = myitem[2]

####### puts sequence in correct orientation; if wrong direction exonerate gets confused
					if myitem[3] > myitem[4]:
						genomeseq = genomeseq + reverse_complement(fastadict[contigname])
					else:
						genomeseq = genomeseq + fastadict[contigname]							


			
				tempgenome = open(sys.argv[2] + '.tempgenome', 'w')
				tempgenome.write('>tempgenome\n' )
				tempgenome.write(genomeseq + '\n')


				tempgenome.close()


	

######## run exonerate, the 1 untranslated sequence to 1 constructed 'genomic' sequence. write out the cutting coordinates

				cmd = '/home/phuong/exonerate-2.2.0-x86_64/bin/exonerate --model est2genome myprot.fa ' + sys.argv[2] + '.tempgenome > exoneratefile'
				os.system(cmd)
     	 			all_qresult = list(SearchIO.parse('exoneratefile', 'exonerate-text'))






				if len(seq.strip()) == all_qresult[0][0][0].query_span:
					myout = open(sys.argv[1] + '_venombed', 'a')
					hsp = all_qresult[0][0][0]
					exoncounter = 1
					for i in range(0,len(hsp)):
						start = hsp[i].query_start
						end = hsp[i].query_end
						myout.write(header + '\t' + str(start) + '\t' + str(end) + '\t' + sys.argv[2] + '\texonerated\texon' + str(exoncounter) + '\n')
						exoncounter += 1
					myout.close()
				else:
					mystart = 0
					myend = 0
				
					myout = open(sys.argv[1] + '_venombed', 'a')

					mytracker = 1

					exoncounter = 1

					for item in keeplist:
						if len(keeplist) == 1:
							if (item[0]-mystart) < 5:

								myout.write(header + '\t' + str(mystart) + '\t' + str(item[1]) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')
								exoncounter += 1
								myout.write(header + '\t' + str(item[1]) + '\t' + str(len(seq)) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')
							elif (len(seq) - item[1]) < 5:
								myout.write(header + '\t' + str(mystart) + '\t' + str(item[0]) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')
								exoncounter += 1						
								myout.write(header + '\t' + str(item[0]) + '\t' + str(len(seq)) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')
							else:
								myout.write(header + '\t' + str(mystart) + '\t' + str(item[0]) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) +  '\n')	
								exoncounter += 1						
								myout.write(header + '\t' + str(item[0]) + '\t' + str(item[1]) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')
								exoncounter += 1
								myout.write(header + '\t' + str(item[1]) + '\t' + str(len(seq)) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')

						elif mytracker == len(keeplist):

							if (item[0]-mystart) > 5 and (len(seq) - item[1]) > 5:

								myout.write(header + '\t' + str(mystart) + '\t' + str(item[0]) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')
								exoncounter += 1
								myout.write(header + '\t' + str(item[0]) + '\t' + str(item[1]) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')
								exoncounter += 1
								myout.write(header + '\t' + str(item[1]) + '\t' + str(len(seq)) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')
							elif (item[0]-mystart) > 5:

								myout.write(header + '\t' + str(mystart) + '\t' + str(item[0]) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')
								exoncounter += 1
								myout.write(header + '\t' + str(item[0]) + '\t' + str(item[1]) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')
								exoncounter += 1
						
							elif (len(seq) - item[1]) > 5:

								myout.write(header + '\t' + str(mystart) + '\t' + str(item[1]) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')
								exoncounter += 1
								myout.write(header + '\t' + str(item[1]) + '\t' + str(len(seq)) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')
							else:

								myout.write(header + '\t' + str(mystart) + '\t' + str(len(seq)) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')						

						elif (item[0]-mystart) > 5:
							myout.write(header + '\t' + str(mystart) + '\t' + str(item[0]) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')
							exoncounter += 1

							myout.write(header + '\t' + str(item[0]) + '\t' + str(item[1]) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')
							mystart = item[1]
							mytracker += 1
							exoncounter += 1
						else:

							myend = item[1]	
							myout.write(header + '\t' + str(mystart) + '\t' + str(myend) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')

							mystart = item[1]
							mytracker += 1
							exoncounter += 1
					myout.close()



			else:

###################### create bed file based on bed coordinates

				mystart = 0
				myend = 0
				
				myout = open(sys.argv[1] + '_venombed', 'a')

				mytracker = 1

				exoncounter = 1

				for item in keeplist:
					if len(keeplist) == 1:
						if (item[0]-mystart) < 5:

							myout.write(header + '\t' + str(mystart) + '\t' + str(item[1]) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')
							exoncounter += 1
							myout.write(header + '\t' + str(item[1]) + '\t' + str(len(seq)) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')
						elif (len(seq) - item[1]) < 5:
							myout.write(header + '\t' + str(mystart) + '\t' + str(item[0]) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')
							exoncounter += 1						
							myout.write(header + '\t' + str(item[0]) + '\t' + str(len(seq)) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')
						else:
							myout.write(header + '\t' + str(mystart) + '\t' + str(item[0]) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) +  '\n')	
							exoncounter += 1						
							myout.write(header + '\t' + str(item[0]) + '\t' + str(item[1]) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')
							exoncounter += 1
							myout.write(header + '\t' + str(item[1]) + '\t' + str(len(seq)) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')

					elif mytracker == len(keeplist):

						if (item[0]-mystart) > 5 and (len(seq) - item[1]) > 5:

							myout.write(header + '\t' + str(mystart) + '\t' + str(item[0]) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')
							exoncounter += 1
							myout.write(header + '\t' + str(item[0]) + '\t' + str(item[1]) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')
							exoncounter += 1
							myout.write(header + '\t' + str(item[1]) + '\t' + str(len(seq)) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')
						elif (item[0]-mystart) > 5:

							myout.write(header + '\t' + str(mystart) + '\t' + str(item[0]) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')
							exoncounter += 1
							myout.write(header + '\t' + str(item[0]) + '\t' + str(item[1]) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')
							exoncounter += 1
						
						elif (len(seq) - item[1]) > 5:

							myout.write(header + '\t' + str(mystart) + '\t' + str(item[1]) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')
							exoncounter += 1
							myout.write(header + '\t' + str(item[1]) + '\t' + str(len(seq)) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')
						else:

							myout.write(header + '\t' + str(mystart) + '\t' + str(len(seq)) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')						

					elif (item[0]-mystart) > 5:
						myout.write(header + '\t' + str(mystart) + '\t' + str(item[0]) + '\t' + sys.argv[2] + '\tdidnotblast\texon' + str(exoncounter) + '\n')
						exoncounter += 1

						myout.write(header + '\t' + str(item[0]) + '\t' + str(item[1]) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')
						mystart = item[1]
						mytracker += 1
						exoncounter += 1
					else:

						myend = item[1]	
						myout.write(header + '\t' + str(mystart) + '\t' + str(myend) + '\t' + sys.argv[2] + '\tblasted\texon' + str(exoncounter) + '\n')

						mystart = item[1]
						mytracker += 1
						exoncounter += 1
				myout.close()



















