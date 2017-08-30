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

	ID = element[1]

	ID2 = element[0]

#	read1 = '/nfs/LabShared/MarkPhuong/exonCapturePilot/1spadesAssemble/' + ID + '_final1.fq',
#	read2 = '/nfs/LabShared/MarkPhuong/exonCapturePilot/1spadesAssemble/' + ID + '_final2.fq',
#	unpaired = '/nfs/LabShared/MarkPhuong/exonCapturePilot/1spadesAssemble/' + ID + '_finalunpaired.fq',

	variables = dict(
	sample = ID,
	ref = ID + '_definedseqs_v5.fa' ,
	read1 = '/pylon2/bi4s86p/phuong/venom/stats/3exon_stats/' + ID2 + '_R1_trimmed.fq',
	read2 = '/pylon2/bi4s86p/phuong/venom/stats/3exon_stats/' + ID2 + '_R2_trimmed.fq',
	out_paired = ID + '_out_venom_paired',
	out_unpaired = ID + '_out_venom_unpaired',
	outfile = ID + '_exon_stats'
	) #name your output



	commands = """
	bowtie2-build {ref} {sample} 
	bowtie2 -x {sample} -1 {read1} -2 {read2} --local --very-sensitive-local --no-discordant -p 15 --score-min L,70,1 -S {out_paired}.sam > {sample}_venom_paired.out 2> {sample}_venom_paired.stderr
	samtools view -bS -@ 15 {out_paired}.sam > {out_paired}.bam
	samtools sort -@ 15 -o {outfile}.bam -O bam {out_paired}.bam
	samtools index {outfile}.bam
	samtools mpileup -d 1000000 -u -I -t DP -t SP -B -A -f {ref} {sample}_exon_stats.bam | /home/phuong/bcftools-1.3.1/bcftools call -c - > {sample}_exon_stats.vcf
	""".format(**variables)

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)



mylist = []
def main():
	args = get_args() 



	with open(args.map) as rfile:
		for line in rfile:
			line = line.strip().split('\t')
			mylist.append(line)
#			align(line)


	pool = multiprocessing.Pool(4)
	pool.map(align, mylist)#run the function with the arguments

if __name__ == "__main__": #run main over multiple processors
	main()









