import os
import sys

myfasta = open('MAP11_definedseqs_v3.fa', 'r')

out = open('mytest.fa', 'w')

for line in myfasta:
	if ">" in line:
		info = line.strip()[1:].split('|')

		out.write('>' +'|'.join(info[1:]) + '|' +  info[0] + '\n')
		out.write(next(myfasta))