


counter = 0
while counter < 4:
	mybatch = open('venomdistbatch', 'r')

	out = open('venomdistbatch' + str(counter), 'w')

	for line in mybatch:
		if 'mapfile' in line:
			line = line.replace('mapfile', 'mapfile.pdist.venom' + str(counter))
			out.write(line)
		else:
			out.write(line)
	out.close()
	counter += 1
