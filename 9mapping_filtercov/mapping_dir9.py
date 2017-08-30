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
	ref = ID + '_definedseqs_v2.fa' ,
	read1 = ID + '_venomreads1.fq',
	read2 = ID + '_venomreads2.fq',
	unpaired = ID + '_venomreadsunpaired.fq',
	out_paired = ID + '_out_venom_paired',
	out_unpaired = ID + '_out_venom_unpaired',
	outfile = ID + '_venom_sorted'
	) #name your output

#	python cut_proteins.py {sample}_definedseqs.fa {ref}
#	samtools index {sample}_md_A_super_v2.bam

	commands = """
	bowtie2-build {ref} {sample} 
	bowtie2 -x {sample} -1 {read1} -2 {read2} --local --very-sensitive-local --no-discordant -p 15 --score-min L,70,1 -S {out_paired}.sam > {sample}_venom_paired.out 2> {sample}_venom_paired.stderr
	bowtie2 -x {sample} -U {unpaired} --local --very-sensitive-local --no-discordant -p 15 --score-min L,70,1 -S {out_unpaired}.sam > {sample}_venom_unpaired.out 2> {sample}_venom_unpaired.stderr
	samtools view -bS -@ 15 {out_paired}.sam > {out_paired}.bam
	samtools view -bS -@ 15 {out_unpaired}.sam > {out_unpaired}.bam
	samtools merge -f {sample}.raw.bam {out_paired}.bam {out_unpaired}.bam
	samtools sort -@ 15 -o {outfile}.bam -O bam {sample}.raw.bam 
	samtools index {outfile}.bam
	java -jar $PICARD_HOME/picard.jar MarkDuplicates INPUT={outfile}.bam OUTPUT={sample}_md_dir9.bam REMOVE_DUPLICATES=TRUE ASSUME_SORTED=TRUE METRICS_FILE={sample}_md_dir9.metrics
	samtools index {sample}_md_dir9.bam
	samtools mpileup -d 1000000 -u -I -t DP -t SP -B -A -f {ref} {sample}_md_dir9.bam | /home/phuong/bcftools-1.3.1/bcftools call -c - > {sample}_dir9.vcf
	rm {out_paired}.sam {out_paired}.bam {out_unpaired}.sam {out_unpaired}.bam {sample}.raw.bam
	python makeVCFcov.py {ref} {sample}_dir9.vcf {sample}_dir9.cov
	python get_alternative_alleles.py {sample} {sample}_dir9.vcf
	python filter_low_cov.py {sample}
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









