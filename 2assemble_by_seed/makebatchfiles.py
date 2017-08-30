


counter = 0
while counter < 32:
	mybatch = open('reassemblebatch', 'r')

	out = open('reassemblebatch' + str(counter), 'w')

	for line in mybatch:
		if 'maptest' in line:
			line = line.replace('maptest', 'mapfile' + str(counter))
			out.write(line)
		else:
			out.write(line)
	out.close()
	counter += 1