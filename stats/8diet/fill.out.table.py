import os
import sys


myfile = open('conus.prey.txt' ,'r')

preylist = []
categories = []
for line in myfile:
	info = line.strip().split('\t')
	categories.append(info[1])
	if info[1] == 'diet specificity':
		preylist.append(info[2])

print set(categories)

firstout = open('preylist', 'w')

for thing in set(preylist):
	firstout.write(thing + '\n')