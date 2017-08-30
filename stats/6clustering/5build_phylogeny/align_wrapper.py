#!/usr/bin/env python


import os
import sys
import argparse
import multiprocessing

def get_args(): #arguments needed to give to this script
        parser = argparse.ArgumentParser(description="run novoalign")

        #forces required argument to let it run
        required = parser.add_argument_group("required arguments")
        required.add_argument("--map", help="textfile with samples to run and what fasta file to match it to", required=True) #A map file with the sample ID and the fasta file it goes to

        return parser.parse_args()


def align(element):

	ID = element





	variables = dict(
	ID = element
	) #name your output


	commands = """
	python grab.genefamilies.py {ID}
	makeblastdb -dbtype nucl -in {ID}.superfamily.fa
	blastn -query {ID}.superfamily.fa -db {ID}.superfamily.fa -outfmt 6 -out {ID}.selfblast -evalue 1e-10 -word_size 11
	python find.best.cluster.py {ID}.superfamily.fa {ID}.selfblast {ID}
	mafft --auto {ID}.align.these.first > {ID}.align.these.first.aligned
	mafft --add {ID}.add.these.later {ID}.align.these.first.aligned > {ID}.allsequences.aligned
 	cp {ID}*.aligned /pylon2/bi4s86p/phuong/venom/stats/6clustering/5build_phylogeny/aligned
	cp {ID}.selfblast /pylon2/bi4s86p/phuong/venom/stats/6clustering/5build_phylogeny/blastfiles
        cp {ID}.superfamily.fa* /pylon2/bi4s86p/phuong/venom/stats/6clustering/5build_phylogeny/blastfiles
	cp {ID}.align.these.first /pylon2/bi4s86p/phuong/venom/stats/6clustering/5build_phylogeny/inputfiles
        cp {ID}.add.these.later /pylon2/bi4s86p/phuong/venom/stats/6clustering/5build_phylogeny/inputfiles
	cp {ID}.stats /pylon2/bi4s86p/phuong/venom/stats/6clustering/5build_phylogeny/
	""".format(**variables)
#        raxmlHPC -T 10 -n {ID} -s {ID}.allsequences.aligned -x 12345 -N 100 -p 12345 -f a -m GTRGAMMA

	


	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)



mylist = []
def main():
        args = get_args()

        #Make a list of lists, each list within the list will have the first and second elements of the map file that are separated by a tab

        with open(args.map) as rfile:
                for line in rfile:
                        line = line.strip()
#			align(line)
                        mylist.append(line)

        pool = multiprocessing.Pool(10)
        pool.map(align, mylist)#run the function with the arguments

if __name__ == "__main__": #run main over multiple processors
        main()








