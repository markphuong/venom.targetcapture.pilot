import os
import sys




myblast = open(sys.argv[1] + '.venom_exon.blastoutput', 'r')

alreadyseen = []

out = open(sys.argv[1] + '.venomexon.filtered.blastoutput' ,'w')
fail = open(sys.argv[1] + '.blastfail' ,'w')

for line in myblast:
	info = line.strip().split('\t')
	if info[0] in alreadyseen:
		continue
	else:
		if int(info[8]) > int(info[9]):
			start = int(info[9]) - 1
			end = int(info[8])
		else:
			start = int(info[8]) - 1
			end = int(info[9])

		exonstart = int(info[1].split('|')[-2])
		exonend = int(info[1].split('|')[-1])

		if start <= exonstart and end >= exonend:
			out.write(line)
		else:
			fail.write(line)
		alreadyseen.append(info[0])
