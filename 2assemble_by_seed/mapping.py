#!/usr/bin/env python


import os
import sys
import argparse
import multiprocessing



def align(element):

	ID = element



#	read1 = '/nfs/LabShared/MarkPhuong/exonCapturePilot/1spadesAssemble/' + ID + '_final1.fq',
#	read2 = '/nfs/LabShared/MarkPhuong/exonCapturePilot/1spadesAssemble/' + ID + '_final2.fq',
#	unpaired = '/nfs/LabShared/MarkPhuong/exonCapturePilot/1spadesAssemble/' + ID + '_finalunpaired.fq',

	variables = dict(
	sample = ID,
	ref = ID + '_seeds_merged',
	read1 = ID + '_venomreads1.fq',
	read2 = ID + '_venomreads2.fq',
	unpaired = ID + '_venomreadsunpaired.fq',
	out_paired = ID + '_out_venom_paired',
	out_unpaired = ID + '_out_venom_unpaired',
	outfile = ID + '_venom_sorted'
	) #name your output


	commands = """
	bowtie2-build {ref} {sample}
	bowtie2 -x {sample} -1 {read1} -2 {read2} --local --very-sensitive-local --no-discordant -p 3 -S {out_paired}.sam > {sample}_venom_paired.out 2> {sample}_venom_paired.stderr
	bowtie2 -x {sample} -U {unpaired} --local --very-sensitive-local --no-discordant -p 3 -S {out_unpaired}.sam > {sample}_venom_unpaired.out 2> {sample}_venom_unpaired.stderr
	samtools view -bS -@ 3 {out_paired}.sam > {out_paired}.bam
	samtools view -bS -@ 3 {out_unpaired}.sam > {out_unpaired}.bam
	samtools merge -f {sample}.raw.bam {out_paired}.bam {out_unpaired}.bam
	samtools sort -@ 3 -o {outfile}.bam -O bam {sample}.raw.bam 
	samtools index {outfile}.bam
	rm {out_paired}.sam {out_paired}.bam {out_unpaired}.sam {out_unpaired}.bam {sample}.raw.bam
	""".format(**variables)

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)



align(sys.argv[1])








