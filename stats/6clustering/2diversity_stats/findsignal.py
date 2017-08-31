import os
import sys

myfunction = open('functional.region.to.exon.structure.reference', 'r')

for line in myfunction:
	if "signal" in line:
		if '|exon1' in line:
			continue
		else:
			print line