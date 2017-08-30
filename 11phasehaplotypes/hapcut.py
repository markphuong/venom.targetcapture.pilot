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




	variables = dict(
	sample = ID) #name your output

	commands = """
	/home/phuong/hapcut2/build/extractHAIRS --VCF {sample}_dir10_vars.vcf --bam {sample}_md_dir10.bam --maxIS 600 > {sample}_fragment_matrix_file
	/home/phuong/hapcut2/build/HAPCUT2 --fragments {sample}_fragment_matrix_file --VCF {sample}_dir10_vars.vcf --output {sample}_output_haplotype_file > {sample}.hapcut.log
	python get_haplotypes.py {sample} {sample}_definedseqs_v5.fa
	/home/phuong/cd-hit-v4.6.4-2015-0603/cd-hit-est -i {sample}_haplotypes.fa -o {sample}_phased_haps_merged.fa -c 1	
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
#			align(line)
			mylist.append(line)


	pool = multiprocessing.Pool(1)
	pool.map(align, mylist)#run the function with the arguments

if __name__ == "__main__": #run main over multiple processors
	main()









