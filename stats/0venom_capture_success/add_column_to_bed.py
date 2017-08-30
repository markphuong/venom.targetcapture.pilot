import os
import sys


mybed = open(sys.argv[1], 'r')


mydict = dict()

for line in mybed:
	info = line.strip().split('\t')[0]

	if info in mydict:
		mydict[info] += 1
	else:
		mydict[info] = 1

mybed.close()


out = open(sys.argv[2], 'w')

mybed = open(sys.argv[1], 'r')


for line in mybed:
	info = line.strip().split('\t')[0]	

	output = line.strip() + '\t' + str(mydict[info]) + 'pieces' + '\n'

	out.write(output)
