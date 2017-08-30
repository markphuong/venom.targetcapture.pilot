import os
import sys

thedir = [f for f in os.listdir('.') if os.path.isfile(f)]


out = open('A_superfamily.fa', 'w')

for thing in thedir:
	if 'v6.fa' in thing:
		myfasta = open(thing, 'r')

		for line in myfasta:
			if '>' in line:
				if "|A|exon2" in line:
					out.write(line)
					out.write(next(myfasta))

		myfasta.close()