import os
import sys

thedir = [f for f in os.listdir('.') if os.path.isfile(f)]


out = open('A_superfamily.fa', 'w')

for thing in thedir:
	if 'analyzethese.fa' in thing:
		myfasta = open(thing, 'r')

		for line in myfasta:
			if '>' in line:
				if "|A_exon1" in line:
					out.write(line)
					out.write(next(myfasta))

		myfasta.close()
