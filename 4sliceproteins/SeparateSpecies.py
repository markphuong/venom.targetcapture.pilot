#!/usr/bin/env python


import os
import sys
import argparse
import multiprocessing
from collections import defaultdict



specieslist = ['virgo', 'marmoreus', 'californicus', 'quercinus', 'ebraeus', 'lividus', 'rattus', 'sponsalis', 'imperialis', 'varius', 'arenatus', 'coronatus']

for species in specieslist:
	outname = species + '_venomprots.fa'

	out = open(outname, 'w')

	rfile = open('all_proteins_renamed.fa', 'r')

	for line in rfile:
		if ">" in line:

			info = line.strip().split('|')
			spname = info[1]
			if 'DivMKLLLTLLLG' in line and species == spname:
				print line
			if species == spname:
				out.write(line)
				out.write(next(rfile))
			else:
				continue
		else:
			continue

	outname2 = species + '_extractedseq.fa'

	out2 = open(outname2, 'w')

	rfile2 = open('all_extractedseq_renamed.fa', 'r')

	for line in rfile2:
		if ">" in line:

			info = line.strip().split('|')
			spname = info[1]
			if 'DivMKLLLTLLLG' in line and species == spname:
				print line
			if species == spname:
				out2.write(line)
				out2.write(next(rfile2))
			else:
				continue
		else:
			continue



