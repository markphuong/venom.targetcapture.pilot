#!/usr/bin/env python


import os
import sys
import argparse
import multiprocessing

def get_args(): 
	parser = argparse.ArgumentParser(description="run novoalign")

	#forces required argument to let it run
	required = parser.add_argument_group("required arguments") 
	required.add_argument("--map", help="textfile with samples to run and what fasta file to match it to", required=True) 

	return parser.parse_args()


def align(element):

	ID = element



#	read1 = '/nfs/LabShared/MarkPhuong/exonCapturePilot/1spadesAssemble/' + ID + '_final1.fq',
#	read2 = '/nfs/LabShared/MarkPhuong/exonCapturePilot/1spadesAssemble/' + ID + '_final2.fq',
#	unpaired = '/nfs/LabShared/MarkPhuong/exonCapturePilot/1spadesAssemble/' + ID + '_finalunpaired.fq',

	variables = dict(
	sample = ID,
	ref = ID + '_venom_phylo_combined.fa' ,
	read1 = '/pylon2/bi4s86p/phuong/venom/fastqfiles/' + ID + '_final1.fq',
	read2 = '/pylon2/bi4s86p/phuong/venom/fastqfiles/' + ID + '_final2.fq',
	unpaired = '/pylon2/bi4s86p/phuong/venom/fastqfiles/' + ID + '_finalunpaired.fq',
	out_paired = ID + '_out_venom_paired',
	out_unpaired = ID + '_out_venom_unpaired',
	outfile = ID + '_capture_stats'
	) #name your output

#	python cut_proteins.py {sample}_definedseqs.fa {ref}
#	samtools index {sample}_md_A_super_v2.bam

	commands = """
	cat {sample}_phylo_contigs.fasta {sample}_definedseqs_v5.fa > {sample}_venom_phylo_combined.fa
	bowtie2-build {ref} {sample} 
	bowtie2 -x {sample} -1 {read1} -2 {read2} --local --very-sensitive-local --no-discordant -p 15 --score-min L,70,1 -S {out_paired}.sam > {sample}_venom_paired.out 2> {sample}_venom_paired.stderr
	bowtie2 -x {sample} -U {unpaired} --local --very-sensitive-local --no-discordant -p 15 --score-min L,70,1 -S {out_unpaired}.sam > {sample}_venom_unpaired.out 2> {sample}_venom_unpaired.stderr
	samtools view -bS -@ 15 {out_paired}.sam > {out_paired}.bam
	samtools view -bS -@ 15 {out_unpaired}.sam > {out_unpaired}.bam
	samtools merge -f {sample}.raw.bam {out_paired}.bam {out_unpaired}.bam
	samtools sort -@ 15 -o {outfile}.bam -O bam {sample}.raw.bam 
	samtools index {outfile}.bam
	java -jar $PICARD_HOME/picard.jar MarkDuplicates INPUT={outfile}.bam OUTPUT={sample}_md_capstats.bam REMOVE_DUPLICATES=FALSE ASSUME_SORTED=TRUE METRICS_FILE={sample}_md_capstats.metrics
	samtools index {sample}_md_capstats.bam
	samtools mpileup -d 1000000 -u -I -t DP -t SP -B -A -f {ref} {sample}_md_capstats.bam | /home/phuong/bcftools-1.3.1/bcftools call -c - > {sample}_capstats.vcf
	python makeVCFcov.py {ref} {sample}_capstats.vcf {sample}_capstats.cov
	python generate_coverage_per_locus.py {sample}
	rm {out_paired}.sam {out_paired}.bam {out_unpaired}.sam {out_unpaired}.bam {sample}.raw.bam
	""".format(**variables)

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)



mylist = []
def main():
	args = get_args() 



	with open(args.map) as rfile:
		for line in rfile:
			line = line.strip()
			mylist.append(line)
#			align(line)


	pool = multiprocessing.Pool(4)
	pool.map(align, mylist)#run the function with the arguments

if __name__ == "__main__": #run main over multiple processors
	main()









