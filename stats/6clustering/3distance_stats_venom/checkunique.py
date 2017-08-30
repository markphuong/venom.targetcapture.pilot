import os
import sys


mymap = open('all.venom.datapoints', 'r')

mylist = []

for line in mymap:
	mylist.append(line.strip())

print len(mylist)

print len(list(set(mylist)))