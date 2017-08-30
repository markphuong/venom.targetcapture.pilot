import pysam
import os
import sys


SampleID = sys.argv[1]

samfile = pysam.AlignmentFile(SampleID + '_venom_sorted.bam', "rb")


myseeds = open(SampleID + '_seeds_merged', 'r')

os.system('touch ' + SampleID + '_venom_contigs_reassembled.fa')

mydir = os.getcwd() + '/' + SampleID + '_tempdir/contigs.fasta'

#for each seed, subset venom reads that mapped to that seed, and assemble them, and save all the assembled contigs
for line in myseeds:
	if ">" in line:

		seq = next(myseeds)

		myseq = len(seq.strip())		

		seedname = line.strip()[1:]
		myIDlist = open(SampleID + '_reads_to_reassemble_list_orig', 'w')


		for read in samfile.fetch(seedname):
			myIDlist.write(read.query_name + '\n')
			myIDlist.write(read.query_name + '/1' + '\n')
			myIDlist.write(read.query_name + '/2' + '\n')

		myIDlist.close()


		tempseed = open(SampleID + '_' +seedname + '_mytempseed.fa', 'w')

		tempseed.write(line)
		tempseed.write(seq)
		tempseed.close()

		variables = dict(
		sample = SampleID,
		seed = seedname)


		commands = """
		/home/phuong/bbmap/filterbyname.sh in={sample}_venomreads1.fq in2={sample}_venomreads2.fq out={sample}_reassemble1.fq out2={sample}_reassemble2.fq names={sample}_reads_to_reassemble_list_orig substring=f include=t ow=t
		""".format(**variables)

		cmd_list = commands.split("\n")
		for cmd in cmd_list:
			os.system(cmd)

		mympivalues = [90, 92, 94, 96, 98]

		for value in mympivalues:

			variables = dict(
			sample = SampleID,
			seed = seedname,
			mpi = value,
			myseq = myseq + 1
			)		
			commands = """
			/home/phuong/PriceSource140408/PriceTI -fpp {sample}_reassemble1.fq {sample}_reassemble2.fq 500 95 -icf {sample}_{seed}_mytempseed.fa 1 1 5 -nc 5 -mol 40 -tol 20 -mpi {mpi} -target 90 2 -lenf {myseq} 4 -o {sample}_mycontig.fa
			sed -i \'s/>contig/>{seed}_{mpi}/g\' {sample}_mycontig.cycle5.fa
			cat {sample}_mycontig.cycle5.fa >> {sample}_venom_contigs_reassembled.fa

			""".format(**variables)

			cmd_list = commands.split("\n")
			for cmd in cmd_list:
				os.system(cmd)

		commands = """
		rm {sample}_{seed}_mytempseed.fa
		""".format(**variables)

		cmd_list = commands.split("\n")
		for cmd in cmd_list:
			os.system(cmd)









