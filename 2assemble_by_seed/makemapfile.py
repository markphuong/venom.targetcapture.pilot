import os
import sys
from collections import defaultdict
import multiprocessing
from os import listdir
from os.path import isfile, join


mymap = open('mapfile', 'r')



counter = 0
for line in mymap:
	
	out = open('mapfile' + str(counter), 'w')
#	thedir = [f for f in os.listdir('.') if os.path.isfile(f)]

#	for thing in thedir:
#		if line.strip() in thing and 'genefam' in thing:



#			out.write('_'.join(thing.split('_')[0:2])+'\n')


	out.write(line)
	out.close()

	counter += 1