import os
import sys

myfasta = open(sys.argv[1], 'r')

for line in myfasta:
	if ">" in line:
		info = line.strip().split('|')
		start = int(info[-2])
		end = int(info[-1])

		if end - start <= 3:

			print line

		if end < 0 or start <0:
			print line
