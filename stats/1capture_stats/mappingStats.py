import os
import sys
from collections import defaultdict

def align(element):

	element = element.split('_')[0]
	variables = dict(
	ID = element,
	) #name your output

# samtools flagstat summarizes mapping statistics

	commands = """
	samtools flagstat {ID}_md_capstats.bam > {ID}.flagstat
	""".format(**variables)
	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)

#parse mapping statistics

	myflagstat = open(element + '.flagstat', 'r')

	for line in myflagstat:
		if 'mapped' in line and '%' in line:
			myreads = line.split('(')[1].split('%')[0]
			readnum = float(line.split(' +')[0])
		elif 'duplicates' in line:
			duplicates = float(line.split(' +')[0])
		else:
			continue
#	print duplicates
#	print readnum
	mydup = duplicates/readnum

	return [myreads, mydup] ### returns percent reads on target, and percent duplication

thedir = [f for f in os.listdir('.') if os.path.isfile(f)]

out = open('mynuclearstats', 'w')

for thing in thedir:
	if '_md_capstats.bam.bai' in thing:
		print thing

		mylist = []

		mystats = align(thing)

		mylist.append(mystats[0])
		mylist.append(mystats[1])


		myname = thing.split('_')[0]
		mylist.append(myname)
		mylist = [str(item) for item in mylist]
		out.write('\t'.join(mylist)+'\n')
	else:
		continue






