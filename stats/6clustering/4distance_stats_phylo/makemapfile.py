import os
import sys
from collections import defaultdict
import multiprocessing
from os import listdir
from os.path import isfile, join


mymap = open('mapfile', 'r')



counter = 0
mapfilenum =0 
for line in mymap:
	thing = line.strip()

	if counter == 0:
		out = open('mapfile' + str(mapfilenum), 'w')
		out.write(thing + '\n')
		counter += 1
		mapfilenum += 1
	elif counter > 0 and counter < 100000:
		out.write(thing + '\n')
		counter += 1
	else:
		out.write(thing + '\n')
		out.close()
		counter = 0

	
#	out = open('mapfile' + str(counter), 'w')
#	thedir = [f for f in os.listdir('.') if os.path.isfile(f)]

#	for thing in thedir:
#		if line.strip() in thing and 'genefam' in thing:



#			out.write('_'.join(thing.split('_')[0:2])+'\n')


#	out.write(line)
#	out.close()

#	counter += 1
