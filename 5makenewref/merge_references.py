import os
import sys





thedir = [f for f in os.listdir('.') if os.path.isfile(f)]


out = open('all_assembled_venom_contigs.fa', 'w')

for thing in thedir:
	if '.fa.NI.subset' in thing:
		myfasta = open(thing, 'r')

		ID = thing.split('_')[0]

		for line in myfasta:
			if ">" in line:
				header = line.strip().split(' ')[0] + '|' + ID
				out.write(header+'\n')
				out.write(next(myfasta).strip()+'\n')

		myfasta.close()
