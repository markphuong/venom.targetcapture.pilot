import os
import sys


thedir = [f for f in os.listdir('.') if os.path.isfile(f)]


counter = 0

out = open(sys.argv[1] + '_alternative_alleles', 'w')




myvcf = open(sys.argv[2], 'r')

ID = sys.argv[1]

for line in myvcf:
	if "#" in line:
		continue
	else:
		info = line.strip().split('\t')
		if info[4] != '.' and '1/1:' in line:
			out.write(ID + '\t' + info[0] + '\t'+ info[1] + '\t' + info[4] + '\t' + '1/1' + '\n')
		elif info[4] != '.' and '0/1:' in line:
			out.write(ID + '\t' + info[0] + '\t'+ info[1] + '\t' + info[4] + '\t' + '0/1' + '\n')

