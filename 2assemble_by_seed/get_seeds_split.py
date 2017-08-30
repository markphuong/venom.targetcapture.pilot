import pysam
import os
import sys
from collections import defaultdict

def leftit(sequence, start, end,ID):

	mystartlimit = 0

	while len(sequence[start:end]) < 100:
		if start == mystartlimit:
			start = 0
		else:
			start = start - 1



		if len(sequence[start:end]) >= 100:
			break
		elif start == mystartlimit:
			break
		else:
			continue

	mytrffile = open(ID + '_mytrfseq_left.fa','w')
	mytrffile.write('>1\n')
	mytrffile.write(sequence[start:end]+'\n')
	mytrffile.close()

	variables = dict(
	ID = ID)


	commands = """
	/home/phuong/trf409.linux64 {ID}_mytrfseq_left.fa 2 7 7 80 10 12 2 -l 10000 -ngs -h > {ID}_trf_left.output
	""".format(**variables)

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)

	return [start, end]

def rightit(sequence, start, end,ID):

	myendlimit = len(sequence)


	while len(sequence[start:end]) < 100:

		if end == myendlimit:
			end = end
		else:
			end = end + 1

		if len(sequence[start:end]) >= 100:
			break
		elif end == myendlimit:
			break
		else:
			continue

	mytrffile = open(ID + '_mytrfseq_right.fa','w')
	mytrffile.write('>1\n')
	mytrffile.write(sequence[start:end]+'\n')
	mytrffile.close()

	variables = dict(
	ID = ID)


	commands = """
	/home/phuong/trf409.linux64 {ID}_mytrfseq_right.fa 2 7 7 80 10 12 2 -l 10000 -ngs -h > {ID}_trf_right.output
	""".format(**variables)

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)



	return [start, end]


def sam_magic(contigname, mystart, myend, thelength, SampleID, myreadlist):

	samfile = pysam.AlignmentFile(SampleID.split('_')[0] + "_sorted.bam", "rb")

	tempseedout = open(SampleID + '_tempreads.fa', 'w')

### for a particular contig and the venom associated region/exon, save all the read headers and actually write out all the reads that were mappable to this region
	for read in samfile.fetch(contigname, mystart, myend):

		tempseedout.write(">" + read.query_name.replace(':', '_') + '\n')
		tempseedout.write(read.query_sequence + '\n')

		myreadlist.append(read.query_name)

	tempseedout.close()


#perform a cd-hit-est and cap3 to merge and assemble reads into longer contigs (via greedy algorithm, not de bruijn graph assembly. 
	os.system('/home/phuong/cd-hit-v4.6.4-2015-0603/cd-hit-est -i ' + SampleID + '_tempreads.fa -o ' + SampleID + '_reads.cdhit.98percent -c .98 -n 10')
	os.system('/home/phuong/CAP3/cap3 ' + SampleID + '_reads.cdhit.98percent -p 99')
	os.system('cat ' + SampleID + '_reads.cdhit.98percent.cap.contigs ' + SampleID + '_reads.cdhit.98percent.cap.singlets > ' + SampleID + '_reads_cap3_combined')
	os.system('python makesomethingNotInterleaved.py ' + SampleID + '_reads_cap3_combined ' + SampleID + '_reads_cap3_combined.NI')
	os.system('blastn -query ' + SampleID + '_reads_cap3_combined.NI -db ' + SampleID + '_temp.fasta -outfmt 6 -word_size 11 -out ' + SampleID + '_temp.blastoutput -evalue 1e-10')


	my_temp_fasta = open(SampleID + '_reads_cap3_combined.NI', 'r')

#then, only save sequences that match in equal length or greater to the original region that was associated with the venom genes/exon/region
	my_fasta_dict = dict()

	for line in my_temp_fasta:
		if '>' in line:
			my_fasta_dict[line.strip()[1:]] = next(my_temp_fasta).strip()

	my_blast = open(SampleID + '_temp.blastoutput', 'r')

	myseedseqs = []

	for line in my_blast:
		info  = line.strip().split('\t')
		if int(info[3]) >= 100:
			myseedseqs.append(my_fasta_dict[info[0]][int(info[6])-1:int(info[7])])

	os.system('rm ' + SampleID + '*percent.cap*')
	os.system('rm ' + SampleID + '*temp*')
	os.system('rm ' + SampleID + '*cap3_combined*')
	os.system('rm ' + SampleID + '*_reads.cdhit.98percent*')
	return [myseedseqs, myreadlist]








## get sample ID
SampleID = sys.argv[1]
myID = sys.argv[2]

# open a preliminary seeds file. this file contains all seed sequences (any region blastable to venom genes) and other reads assembled via cap3 and cd-hit-est that a) mapped to the same region and b)  match full length of the 'blastable' region
seedout = open(SampleID + '_prelim_seeds', 'w')

#this allows you to get the original sequence that was assembled via SPAdes, only accounting for the part that blasted to the targets
myfasta = open(myID + '_assemblies_clustered.fasta.NI', 'r')

######## initialize dictionary of fasta sequences
fastadict = dict()

for line in myfasta:
	if ">" in line:
		fastadict[line.strip()[1:]] = next(myfasta).strip()

##### loop through blastfile, and if it is a unique blasted region to your venom gene reference, do some pysam magic
#myblast = open(SampleID + '_venom_filtered.blast', 'r')
myblast = open(SampleID + '_filtered.genefam.blast', 'r')

counter = 0 # allows you to number your seeds

readlist = [] # list of all venom reads that you will append as you loop through this file. These reads will >only< be reads that map to a particular venom gene exon

seendict = defaultdict(list) ### allows you to only consider unique blast output

temptemp = open(SampleID + '_startends', 'w')

for line in myblast:
	info = line.strip().split('\t')


		
	if int(info[6]) > int(info[7]):
		start = int(info[7])-1
		end = int(info[6])
		startorig = int(info[7])-1
		endorig = int(info[6])
	else:
		start = int(info[6])-1
		end = int(info[7])
		startorig = int(info[6])-1
		endorig = int(info[7])


	if len(fastadict[info[0]][start:end]) < 100:
		mystartlimit = 0
		myendlimit = len(fastadict[info[0]])

		while len(fastadict[info[0]][start:end]) < 100:
			if start == mystartlimit:
				start = 0
			else:
				start = start - 1

			if end == myendlimit:
				end = end
			else:
				end = end + 1

			if len(fastadict[info[0]][start:end]) >= 100:
				break
			elif start == mystartlimit and end == myendlimit:
				break
			else:
				continue

		mytrffile = open(SampleID + '_mytrfseq.fa','w')
		mytrffile.write('>1\n')
		mytrffile.write(fastadict[info[0]][start:end]+'\n')
		mytrffile.close()

		variables = dict(
		SampleID = SampleID)


		commands = """
		/home/phuong/trf409.linux64 {SampleID}_mytrfseq.fa 2 7 7 80 10 12 2 -l 10000 -ngs -h > {SampleID}_trf.output
		""".format(**variables)

		cmd_list = commands.split("\n")
		for cmd in cmd_list:
			os.system(cmd)

		

		if os.path.getsize(SampleID+'_trf.output') == 0:
			start = start
			end = end
		else:
			mytrffile = open(SampleID+'_trf.output', 'r')

			myperiod = ''

			for line in mytrffile:
				if '@' in line:
					continue
				else:
					myperiod = int(line.strip().split(' ')[2])

			if myperiod == 2:
	

				print line

				leftseq = leftit(fastadict[info[0]], startorig, endorig, SampleID)
				rightseq = rightit(fastadict[info[0]], startorig, endorig, SampleID)

				print fastadict[info[0]][start:end]
				print fastadict[info[0]][leftseq[0]:leftseq[1]]
				print fastadict[info[0]][rightseq[0]:rightseq[1]]

				if os.path.getsize(SampleID+'_trf_left.output') == 0 and len(fastadict[info[0]][leftseq[0]:leftseq[1]]) >= 100:
					start = leftseq[0]
					end = leftseq[1]
					print 'leftseq'
					print start
					print end
				elif os.path.getsize(SampleID+'_trf_right.output') == 0 and len(fastadict[info[0]][rightseq[0]:rightseq[1]]) >= 100:
					start = rightseq[0]
					end = rightseq[1]
					print 'rightseq'
					print start
					print end
				else:
					start = start
					end = end
					print 'origseq'
					print start
					print end
			else:
				start = start
				end = end


	else:
		start = start
		end = end

	temptemp.write(info[0] + '\t' + info[1] + '\t' + info[3] + '\t' + info[6] + '\t' + info[7] + '\t' + str(start) + '\t' + str(end) + '\t' + str(len(fastadict[info[0]][start:end]))+ '\n')
	print len(fastadict[info[0]][start:end])

	if len(fastadict[info[0]][start:end]) < 100:
		continue

	elif info[0] in seendict.keys():
		if [start,end] in seendict[info[0]]:
			continue
		else:
			seendict[info[0]].append([start,end])

### saves the 'seed' sequence from the original exon that was assembled by SPAdes
			seedout.write('>seed_'  + str(counter) + '\n')
			seedout.write(fastadict[info[0]][start:end] + '\n')
			counter +=1

##### opens up a temporary fasta file. You use this later to blast against potential seed sequences to see if they match to the full length of the original sequence
			tempfasta = open(SampleID + '_temp.fasta', 'w')
			tempfasta.write('>temp' + '\n')
			tempfasta.write(fastadict[info[0]][start:end])
			tempfasta.close()
			os.system('makeblastdb -dbtype nucl -in ' + SampleID + '_temp.fasta')

### this contains (a) your seed sequences and (b) your list of venom reads that mapped to the region of the contig that matched your venom targets
			thegoodies = sam_magic(info[0], start, end, end-start, SampleID, readlist)		

			theseedseqs = thegoodies[0]
			readlist = thegoodies[1]

#write out each seed
			for item in theseedseqs:
				seedout.write('>seed_'  + str(counter) + '\n')
				seedout.write(item + '\n')
				counter +=1	

	else:

		seendict[info[0]] = [[start,end]]

		seedout.write('>seed_'  + str(counter) + '\n')
		seedout.write(fastadict[info[0]][start:end] + '\n')
		counter +=1

		tempfasta = open(SampleID + '_temp.fasta', 'w')
		tempfasta.write('>temp' + '\n')
		tempfasta.write(fastadict[info[0]][start:end])
		tempfasta.close()
		os.system('makeblastdb -dbtype nucl -in ' + SampleID + '_temp.fasta')
		
		thegoodies = sam_magic(info[0], start, end, end-start, SampleID, readlist)		

		theseedseqs = thegoodies[0]
		readlist = thegoodies[1]

		for item in theseedseqs:
			seedout.write('>seed_'  + str(counter) + '\n')
			seedout.write(item + '\n')
			counter +=1	

seedout.close()

### merge any redundant sequences, 100% identity threshold to 'unique-ify' the list of seed sequences
os.system('/home/phuong/cd-hit-v4.6.4-2015-0603/cd-hit-est -i ' + SampleID + '_prelim_seeds -o ' + SampleID + '_seeds_merged -c 1 -n 10')


### then, write out all the reads, and pull those reads from the total reads (i.e., subset the venom only reads
venomreads = open(SampleID + '_venom_read_IDs', 'w')

for item in set(readlist):
	venomreads.write(item + '\n')
	venomreads.write(item + '/1' + '\n')
	venomreads.write(item + '/2' + '\n')

venomreads.close()



os.system('/home/phuong/bbmap/filterbyname.sh in=/pylon2/bi4s86p/phuong/venom/fastqfiles/' + myID + '_final1.fq in2=/pylon2/bi4s86p/phuong/venom/fastqfiles/' + myID + '_final2.fq out='+ SampleID + '_venomreads1.fq out2='+ SampleID + '_venomreads2.fq names=' + SampleID + '_venom_read_IDs substring=f include=t ow=t')
os.system('/home/phuong/bbmap/filterbyname.sh in=/pylon2/bi4s86p/phuong/venom/fastqfiles/' + myID + '_finalunpaired.fq out='+ SampleID + '_venomreadsunpaired.fq names=' + SampleID + '_venom_read_IDs substring=f include=t ow=t')

os.system('rm ' + SampleID + '_seeds_merged.clstr')
os.system('rm ' + SampleID + '_venom_read_IDs')




