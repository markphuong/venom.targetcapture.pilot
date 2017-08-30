import os
import sys

myspecies = open('myspecies', 'r')

keeplist = []

for line in myspecies:
	keeplist.append(line.strip())

tax = open('taxonomy', 'r')

out = open('myspecies_andsubgenera.txt', 'w')

for line in tax:
	info = line.strip().split('\t')

	if info[0] in keeplist:
		out.write(line)