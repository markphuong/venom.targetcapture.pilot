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
	/home/phuong/cd-hit-v4.6.4-2015-0603/cd-hit-est -i {ID}.superfamily.fa -o {ID}.superfamily.cdhit -d 0 -c .8 -n 5
	python parse_cluster.py {ID}.superfamily.cdhit.clstr {ID}
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

        pool = multiprocessing.Pool(1)
        pool.map(align, mylist)#run the function with the arguments

if __name__ == "__main__": #run main over multiple processors
        main()








