import os
import sys
from collections import defaultdict
from Bio.Seq import reverse_complement

thedir = [f for f in os.listdir('.') if os.path.isfile(f)]

out = open('cov.stats', 'w')


for thing in thedir:
        if '_coverage' in thing and not '_coverage_' in thing:


                ID = thing.split('_')[0]


                mycov = open(thing, 'r')
		
		covdict = dict()

		totcovcounter = 0
		totcovlength = 0

		venomcovcounter = 0 
		venomcovlength = 0

		phylocovcounter =0 
		phylocovlength = 0
		
                for line in mycov:

			
			
			info = line.strip().split('\t')

			totcovcounter += float(info[-1])
			totcovlength += 1
#			print totcovcounter
#			print line



			if 'seed' in line:
				venomcovcounter += float(info[-1])
				venomcovlength += 1
			else:
				phylocovcounter += float(info[-1])
				phylocovlength += 1				


#		print venomcovcounter
#		print venomcovlength
		out.write(ID + '\t' + str(totcovcounter/totcovlength) + '\t' + str(venomcovcounter/venomcovlength) + '\t' + str(venomcovlength) + '\t' + str(phylocovcounter/phylocovlength) + '\t' + str(phylocovlength) + '\n')




















