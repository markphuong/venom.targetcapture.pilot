myblast = open('MAP48.venomblast', 'r')


for line in myblast:
	info = line.strip().split('\t')
	header = info[0].split('|')
	if header[2] == 'A':
		if int(info[3]) > 100:
			print line.strip()