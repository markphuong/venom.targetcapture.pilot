import os
import sys
from collections import defaultdict

myfasta = open(sys.argv[1], 'r')

mydict = defaultdict(dict)

for line in myfasta:
	if ">" in line:
		if '_1 (' in line:
			info = line.strip().split('_')

			mydict['_'.join(info[0:2])][info[2]] = len(next(myfasta).strip())


myfasta.close()

keeplist = []

for item in mydict.keys():
	keeplist.append(item + '_' + max(mydict[item], key=mydict[item].get))


myfasta = open(sys.argv[1], 'r')

out = open(sys.argv[2], 'w')

for line in myfasta:
	if '_'.join(line.strip().split('_')[0:3]) in keeplist:
		out.write(line)
		out.write(next(myfasta))