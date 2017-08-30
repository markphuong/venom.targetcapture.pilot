import os
import sys


myblast = open(sys.argv[1] + '_venom_filtered.blast', 'r')


for line in myblast:
	info = line.strip().split('\t')


	genefam = info[1].split('|')[2]


	myout = open(sys.argv[1] + '_' + genefam + 'genefam_filtered.blast', 'a')


	myout.write(line)

	myout.close()
