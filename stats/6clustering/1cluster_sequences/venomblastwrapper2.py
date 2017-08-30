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
	blastn -query {ID}_definedseqs_v6.fa -db myregionreference2.fa -outfmt 6 -out {ID}.venom.blastoutput2 -evalue 1e-10 -word_size 11
	python pickbest.py {ID}_definedseqs_v6.fa {ID}.venom.blastoutput2 {ID}_venom_analyzethese.fa 
	python check_failed_sequences.py {ID}_definedseqs_v6.fa {ID}_venom_analyzethese.fa {ID}.failed2
	cp {ID}.venom.blastoutput2 /pylon2/bi4s86p/phuong/venom/stats/6clustering/1cluster_sequences
	cp {ID}_venom_analyzethese.fa /pylon2/bi4s86p/phuong/venom/stats/6clustering/1cluster_sequences
	cp {ID}.failed2 /pylon2/bi4s86p/phuong/venom/stats/6clustering/1cluster_sequences
	""".format(**variables)

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

        pool = multiprocessing.Pool(32)
        pool.map(align, mylist)#run the function with the arguments

if __name__ == "__main__": #run main over multiple processors
        main()








