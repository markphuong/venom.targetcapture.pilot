import os
import sys


mybed = open(sys.argv[1], 'r')


mydict = dict()

for line in mybed:
	info = line.strip().split('\t')

	start = int(info[0].split('|')[4])
	end = int(info[0].split('|')[5])


	myrange1 = range(int(info[1]),int(info[2]))
	myrange2 = range(start, end)


	if len(list(set(myrange1).intersection(myrange2))) == 0:
		continue
	elif info[0] in mydict:
		mydict[info[0]] += 1
	else:
		mydict[info[0]] = 1

mybed.close()


out = open(sys.argv[2], 'w')

mybed = open(sys.argv[1], 'r')

counter = 1
previous = ''
for line in mybed:
	info = line.strip().split('\t')

	start = int(info[0].split('|')[4])
	end = int(info[0].split('|')[5])


	myrange1 = range(int(info[1]),int(info[2]))
	myrange2 = range(start, end)


	if previous == info[0]:
		counter +=1
	else:
		counter = 1

	if len(list(set(myrange1).intersection(myrange2))) == 0:
		continue
	else:

		output = line.strip()[:-1] + str(counter) + '\t' + str(mydict[info[0]]) + 'pieces' + '\n'

		out.write(output)

	previous = info[0]




