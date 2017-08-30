import os
import sys


myfasta = open(sys.argv[1], 'r')
fastadict = dict()

for line in myfasta:
	if ">" in line:
		fastadict[line.strip()[1:]] = next(myfasta).strip()


myblast = open(sys.argv[2], 'r')

out = open(sys.argv[3], 'w')

alreadyseen = []

for line in myblast:
	info = line.strip().split('\t')

	region = info[1].split('|')[-1]

	if info[0] in alreadyseen:
		continue
	elif info[0].split('|')[1] == info[0].split('|')[1]:
		alreadyseen.append(info[0])
		out.write(">" + info[0] + '|' + region + '\n')
		out.write(fastadict[info[0]] + '\n')


	else:
		alreadyseen.append(info[0])		