import os
import sys


mymap = open('mapfile', 'r')

mapfilelist = []

for line in mymap:
	species = line.strip()

	myfasta = open(species + '_venom_analyzethese.fa' , 'r')

	for seq in myfasta:
		if ">" in seq:
			info = seq.strip().split('|')

			mykey = info[1] + '.' + info[-1]

			out = open(mykey + '.superfamily.fa', 'a')

			out.write(seq)
			out.write(next(myfasta))

			out.close()

			mapfilelist.append(mykey)

	myfasta.close()

out2 = open('mapfile.genefamilies', 'w')

for item in sorted(set(mapfilelist)):
	out2.write(item + '\n')

