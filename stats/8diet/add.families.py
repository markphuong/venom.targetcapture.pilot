import os
import sys

############# store diet family map file into dictionary

myfam = open('preylist.families.added', 'r')

famdict = dict()

for line in myfam:
	info = line.strip().split('\t')

	famdict[info[0]] = info[1]


########## add families to each data line

myfile = open('conus.prey.txt', 'r')


families = []

out = open('conus.prey.families.added.txt', 'w')
#print famdict
for line in myfile:
	info = line.strip().split('\t')

	if info[1] == 'diet specificity':
		if info[2] in famdict:
			info[4] = famdict[info[2]]
			families.append(famdict[info[2]])
			out.write('\t'.join(info) + '\n')

		else:
			print line
	else:
		out.write(line)

out.close()

############## store dictionary, key=species, leading to value of families for that species

myfam = open('conus.prey.families.added.txt', 'r')

speciesdict = dict()

specieslist = []

for line in myfam:
	info = line.strip().split('\t')
	if 'Locality' in line:
		continue
	else:
		specieslist.append(info[0])

		if info[1] == 'diet specificity':
			#print line
			if info[4] == "NA":
				continue
			elif info[0] in speciesdict:
				speciesdict[info[0]].append(info[4])
			else:
				speciesdict[info[0]] = [info[4]]

# loop through all species and diet families, create yes/no diet matrix

out2 = open('diet.specificty.traits', 'w')

output = ['Species']

for item in sorted(set(families)):
	if item == 'NA':
		continue
	else:
		output.append(item)

out2.write('\t'.join(output) + '\n')

for species in sorted(set(specieslist)):

	output = [species]

	for family in sorted(set(families)):
		if family == 'NA':
			continue
		elif not species in speciesdict:
			output.append("NA")
		elif family in speciesdict[species]:
			output.append('yes')
		else:
			output.append('no')

	out2.write('\t'.join(output)+'\n')

