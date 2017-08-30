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
	sample = ID,
	name = ID.split('_')[0])



	commands = """
	cp /pylon2/bi4s86p/phuong/venom/2assemble_by_seed/{sample}* ./
	python get_seeds.py {sample}
	python mapping.py {sample}
	python assemble_by_seed.py {sample}
	cp {sample}* /pylon2/bi4s86p/phuong/venom/3reassembled/
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


	pool = multiprocessing.Pool(1)
	pool.map(align, mylist)#run the function with the arguments


if __name__ == "__main__": #run main over multiple processors
	main()







