import os
import sys
from Bio.Seq import reverse_complement
from Bio.Seq import translate
from Bio import SearchIO

########## from past exonerate scripts -- to list exonerate hits descending via bitscores

def myexonerate(exoneratefile):

	out = open('exoneratebed', 'w')
	all_qresult = list(SearchIO.parse(exoneratefile, 'exonerate-vulgar'))

	for i in range(0, len(all_qresult)):

		for k in range(0, len(all_qresult[i])):

			myquery_span = str(all_qresult[i][k][0].query_span)

			myscore = str(all_qresult[i][k][0].score)

			mytarget = all_qresult[i][k].id

			myquery = all_qresult[i].id



			if len(all_qresult[i][k]) > 1:
				print all_qresult[i][k]
				print 'too many hits'
				continue

	#	mystrand = '1'

	#	for item in all_qresult[i][k][0].hit_all:
	#		if 'revcomp' in str(item):
	#			mystrand = '-1'


			strandlist = all_qresult[i][k][0].hit_strand_all
			if len(list(set(strandlist))) == 1:
				mystrand = str(strandlist[0])
			else:
				print 'fuck'

			start =  str(all_qresult[i][k][0].hit_start)
			end = str(all_qresult[i][k][0].hit_end)

			out.write('\t'.join([myquery, mytarget, myquery_span, myscore, mystrand, start, end]) + '\n')
	out.close()

	os.system('sort -k2,2 -k4,4nr -k3,3nr exoneratebed > exoneratebed.sorted')
	

############ load dictionary of assembled contigs

fastadict = dict()

myfasta = open(sys.argv[1], 'r')

for line in myfasta:
	if ">" in line:
		header = line.strip().split(' ')[0][1:]

		fastadict[header] = next(myfasta).strip()

myfasta.close()

########### load reference sequences into a dictionary

refdict = dict()

myref = open(sys.argv[2], 'r')

for line in myref:
	if ">" in line:
		refdict[line.strip()[1:]] = next(myref).strip()

myref.close()

######### load protein reference sequences into a dictionary



protdict = dict()

protfile = open(sys.argv[3],'r')

for line in protfile:
	if ">" in line:
		info = line.strip().split('|')

		protdict[info[0][1:] + '|' + info[-1]] = next(protfile).strip()

protfile.close()

###############

os.system('touch ' + sys.argv[5]) #### load file where you will save blast coordinates of where proteins blasted to particular sequences (as you define exon boundaries

myblast = open(sys.argv[4], 'r') ###### load blast file of best hits

myout = open(sys.argv[6], 'w') ### file with sequences with new headers (which include how the exon boundaries were defined and where they are



########### first step, look through all lines in the filtered blast file
for line in myblast:



	info = line.strip().split('\t')

############# save some important information, like gene family, exon number, the number of pieces, and the original assembled contig name

	genefamily = info[1].split('|')[3]
	exonnumber = info[1].split('|')[4]
	pieces = info[1].split('|')[5]
	myseqheader = info[0]

	myprotheader = info[1].split('|')[1] + '|' + info[1].split('|')[4]


##### did this so that I could refine the boundaries to go all the way to the stop codon if I was alreadyi n the correct frame
	lastexon = 'no'
	if info[1].split('|')[4].replace('exon', '') == info[1].split('|')[5].replace('pieces', ''):
		lastexon = 'yes'


############# write out a file and align (via MAFFT) the query sequence (assembled contig) with the target sequence (reference sequence it blasted to)
	mytempfasta = open('alignthistemp', 'w')



	if int(info[8]) > int(info[9]):
		print 'fuck'
		print line
	else:

		mytempfasta.write('>' + info[1]  + '\n')
		mytempfasta.write(refdict[info[1]] + '\n')
		mytempfasta.write('>' + info[0]  + '\n')
		mytempfasta.write(fastadict[info[0]] + '\n')
	mytempfasta.close()

	cmd = 'mafft --preservecase --auto alignthistemp > outalignedtemp'
	os.system(cmd)

	cmd = 'python makesomethingNotInterleaved.py outalignedtemp outalignedtemp.NI'
	os.system(cmd)

	myaligned = open('outalignedtemp.NI', 'r')




########## open up the alignment file, and find the start and end points of the predicted exon, and recalibrate those positions based on how the alignment added gaps
	myrealstart = ''
	myrealend = ''

	for line in myaligned:
		if '|' in line:
			info = line.strip().split('|')

			start = int(info[-2])
			end = int(info[-1])

			myseq = next(myaligned).strip()
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


############## write out the protein that belongs to the target sequence (because the target sequence is a full locus [exon + intron]) and you want to blast the query sequence (assembled contig) to all proteins that have identical pieces/exon value 
			out = open('mytempprot', 'w')
			for key in refdict:
				if '|' + genefamily + '|' in key and '|' + exonnumber + '|' in key and '|' + pieces + '|' in key:
					
					header = key.split('|')[1] + '|' + key.split('|')[4]


					out.write('>' + header + '\n')
					out.write(protdict[header]+'\n')
				
			out.close()

			myproteinlength = len(protdict[header])
		elif '>' in line:


################### in the query sequence (assembled venom contig), get the start and beginning positions of the aligned region (that matched the exon defined region in the reference) and add 30 bp to each side if possible, for further blasting with a protein	
			header = line.strip()[1:]
			seq = next(myaligned).strip()

			seq = seq[myrealstart:myrealend].replace('-', '')
			origseq = fastadict[header]

			myexonstart = origseq.index(seq)
			myexonend = origseq.index(seq) + len(seq)

			myguessstart = origseq.index(seq) ######### when all else fails, use a simple guess to guess the exon region
			myguessend = origseq.index(seq) + len(seq) ##########  when all else fails, use a simple guess to guess the exon region


			if myexonstart-30 < 0:
				myexonstart = 0
			else:
				myexonstart = myexonstart - 30

			if myexonend+30 < len(fastadict[header]):
				myexonend = myexonend + 30
			else:
				myexonend = len(fastadict[header])
			

################## write out that temporary sequence. you did this so that you limited the search space to a region around the exon to avoid spurius matches
			out = open('mytempexon', 'w')

			out.write('>' + header + '\n')


			out.write(fastadict[header][myexonstart:myexonend] + '\n')	
			
			out.close()

			mywrittenseq = fastadict[header][myexonstart:myexonend]
	myaligned.close()

################################### run tblastn, blastx, and exonerate. Pick the one that had at least 70% of the protein blasted/exonerated. If not, just use the 'guess' option -- which was guessed through a mafft alignment
	pickdict = {'temptblastnoutput':0, 'tempblastxoutput':0 , 'exonerate':0} ###### this dictionary will be filled with alignment lengths

	os.system('makeblastdb -dbtype nucl -in mytempexon')
	os.system('makeblastdb -dbtype prot -in mytempprot')
	os.system('tblastn -query mytempprot -db mytempexon -outfmt 6 -out temptblastnoutput')
	os.system('blastx -query mytempexon -db mytempprot -outfmt 6 -out tempblastxoutput')
	os.system('/home/phuong/exonerate-2.2.0-x86_64/bin/exonerate --model protein2genome mytempprot mytempexon -s 50 --showalignment FALSE > exoneratefile')
	myexonerate('exoneratefile')
	os.system('sort -k11,11g -k4,4nr temptblastnoutput > temptblastnoutput2')
	os.system('mv temptblastnoutput2 temptblastnoutput')
####### find alignment lengths

	protlengthdict = {'temptblastnoutput':0, 'tempblastxoutput':0 , 'exonerate':0}
	headerdict = {'temptblastnoutput':'', 'tempblastxoutput':'' , 'exonerate':''}
	linedict = {'temptblastnoutput':'', 'tempblastxoutput':'' , 'exonerate':''}
	startdict = {'temptblastnoutput':'', 'tempblastxoutput':'' , 'exonerate':''}
	enddict = {'temptblastnoutput':'', 'tempblastxoutput':'' , 'exonerate':''}

	if os.stat('exoneratebed.sorted').st_size == 0:
		pickdict['exonerate'] = 0
	else:
		myexoneratefile = open('exoneratebed.sorted', 'r')

		exoneratetemp = myexoneratefile.readline().strip().split('\t')
		exoneratestart = int(exoneratetemp[-2])
		exonerateend = int(exoneratetemp[-1])

		pickdict['exonerate'] = int(exoneratetemp[2])
		protlengthdict['exonerate'] = len(protdict[exoneratetemp[0]])
		headerdict['exonerate'] = exoneratetemp[0]
		linedict['exonerate'] = '\t'.join(exoneratetemp) + '\n'
		startdict['exonerate'] = int(exoneratetemp[-2])
		enddict['exonerate'] = int(exoneratetemp[-1])
		myexoneratefile.close()

	if os.stat('temptblastnoutput').st_size == 0:
		pickdict['tempblastnoutput'] = 0
	else:
		file1 = open('temptblastnoutput')
		temp1 = file1.readline().strip().split('\t')


		pickdict['temptblastnoutput'] = int(temp1[3])
		protlengthdict['temptblastnoutput'] = len(protdict[temp1[0]])
		headerdict['temptblastnoutput'] = temp1[0]
		linedict['temptblastnoutput'] = '\t'.join(temp1) + '\n'
		startdict['temptblastnoutput'] = int(temp1[8])-1
		enddict['temptblastnoutput'] = int(temp1[9])

		file1.close()

	if os.stat('tempblastxoutput').st_size == 0:
		pickdict['tempblastxoutput'] = 0
	else:
		file2 = open('tempblastxoutput')
		temp2 = file2.readline().strip().split('\t')

		pickdict['tempblastxoutput'] = int(temp2[3])
		protlengthdict['tempblastxoutput'] = len(protdict[temp2[1]])
		headerdict['tempblastxoutput'] = temp2[1]
		linedict['tempblastxoutput'] = '\t'.join(temp2) + '\n'
		startdict['tempblastxoutput'] = int(temp2[6])-1
		enddict['tempblastxoutput'] = int(temp2[7])	
		file2.close()




	pickthisfile = max(pickdict, key=pickdict.get)



######## if less than 70% of the protein was blasted, then a guess is better

	if pickdict[pickthisfile] == 0 or float(pickdict[pickthisfile])/float(protlengthdict[pickthisfile]) < .7:


		start = myguessstart
		end = myguessend
		myout.write('>' + '|'.join([myseqheader, genefamily, exonnumber, pieces, str(start), str(end), 'guessed']) + '\n')
		myout.write(fastadict[myseqheader]+ '\n')
		
	else:


		start = startdict[pickthisfile]
		end = enddict[pickthisfile]

		savedblast = open(sys.argv[5], 'a')
		savedblast.write(linedict[pickthisfile])
		savedblast.close()



		blastedregion = mywrittenseq[start:end]



		start = fastadict[myseqheader].index(blastedregion)
		end = start + len(blastedregion)


########## if blasted to the exon containing a stop codon, try to extend to the stop codon. If not possible, just keep the original start and end
		if lastexon == 'yes':
			findstopseq = translate(fastadict[myseqheader][start:])	

			if '*' in findstopseq:

				if findstopseq.index('*')*3 + start + 3 <= end:
					end = end
				else:
					end = findstopseq.index('*')*3 + 3 + start
				myout.write('>' + '|'.join([myseqheader, genefamily, exonnumber, pieces, str(start), str(end), pickthisfile.replace('temp','').replace('output','')]) + '\n')
				myout.write(fastadict[myseqheader]+ '\n')

				print translate(fastadict[myseqheader][start:end])
				print fastadict[myseqheader][start:end]
			else:
				myout.write('>' + '|'.join([myseqheader, genefamily, exonnumber, pieces, str(start), str(end), pickthisfile.replace('temp','').replace('output','')]) + '\n')
				myout.write(fastadict[myseqheader]+ '\n')
	
		else:


			myout.write('>' + '|'.join([myseqheader, genefamily, exonnumber, pieces, str(start), str(end), pickthisfile.replace('temp','').replace('output','')]) + '\n')
			myout.write(fastadict[myseqheader]+ '\n')

myblast.close()























