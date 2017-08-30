import os
import sys
from collections import defaultdict

mybedutr = open(sys.argv[1], 'r')

myutrdict = defaultdict(dict)

keepdict = dict()

for line in mybedutr:
	info = line.strip().split('\t')

	start = int(info[1])
	end = int(info[2])

	codingstart = int(info[0].split('|')[-3])
	codingend = int(info[0].split('|')[-2])

	transcriptID = info[0].split('|')[-1] + '|' + info[0].split('|')[3].split('_')[0]

	exon = info[5]
	pieces = info[6]


	if transcriptID.split('|')[0] == info[0].split('|')[0]:

		myutrdict[transcriptID][exon] = line


		if exon == 'exon1':		
			if 'blasted' in line or 'exonerated' in line: 
				if (end-codingstart) > 3:

					if transcriptID in keepdict:
						keepdict[transcriptID] += 1
					else:
						keepdict[transcriptID] = 1
				else:
					continue
			else:
				continue
		elif exon.replace('exon','') == pieces.replace('pieces',''):
			if 'blasted' in line or 'exonerated' in line: 
				if (end-codingstart) > 3:

					if transcriptID in keepdict:
						keepdict[transcriptID] += 1
					else:
						keepdict[transcriptID] = 1
				else:
					continue
			else:
				continue
		elif 'blasted' in line or 'exonerated' in line:
			if transcriptID in keepdict:
				keepdict[transcriptID] += 1
			else:
				keepdict[transcriptID] = 1
		else:
			continue	
	else:
		continue						


mybed = open(sys.argv[2])

mybeddict = defaultdict(dict)

counterdict = dict()

for line in mybed:
	info = line.strip().split('\t')
	transcriptID = info[0].split('|')[0] + '|' + info[0].split('|')[3]
	exon = info[5]

	mybeddict[transcriptID][exon] = line

	if 'didnotblast' in line:
		continue
	else:
		if transcriptID in counterdict:
			counterdict[transcriptID] += 1
		else:
			counterdict[transcriptID] = 1			

out = open(sys.argv[3], 'w')

for transcript in sorted(counterdict):
	if transcript in keepdict:
		if keepdict[transcript] > counterdict[transcript]:
			for exon in sorted(myutrdict[transcript]):
				out.write(myutrdict[transcript][exon])
		else:
			for exon in sorted(mybeddict[transcript]):
				out.write(mybeddict[transcript][exon])			
	else:
		for exon in sorted(mybeddict[transcript]):
			out.write(mybeddict[transcript][exon])	











