import os
import sys


#### list of loci with 80% capture success
captureableloci = ["DivMRFYIGLMAA", 
"I3", 
"I2", 
"MMLFM", 
"MNCYL", 
"B1", 
"J", 
"O1", 
"O3", 
"M", 
"O2", 
"D", 
"I1", 
"V", 
"conkunitzin", 
"A", 
"B4", 
"C", 
"conodipine", 
"conohyal", 
"conophysin", 
"conoporin", 
"DivMKLCVVIVLL", 
"DivMKVAVVLLVS", 
"DivMRFLHFLIVA", 
"DivMSKLVILAVL", 
"DivMTLTFLLVVA", 
"E", 
"H", 
"I4", 
"MEVKM", 
"MTFYL", 
"S", 
"Y"]



myfile = open('diversity_stats_transposed.txt', 'r')

out = open('gene.family.sizes.all' , 'w')

out2 = open('gene.family.sizes.70percent', 'w')

out3 = open('gene.family.sizes.captureable', 'w')

counter = 0

exoncounter = 0


for line in myfile:
	if 'species' in line:
		info = line.strip().split('\t')
		info.insert(1, info[0])

		out.write('\t'.join(info) + '\n')
		out2.write('\t'.join(info) + '\n')
		out3.write('\t'.join(info) + '\n')
	elif 'signal' in line or 'onepiece' in line:
		info = line.strip().split('\t')

		info.insert(1, info[0])


#		print info.count('0')

		
		if 'conkunitzin_signal' in line:
			mysignal = line.strip().split('\t')
			continue
		elif 'conkunitzin_onepiece' in line:
			myonepiece = line.strip().split('\t')
			continue
		else:

			exoncounter += 1
			if info.count('0') == 31:
				counter += 1
				continue
			else:
				if info[0].split('_')[0] in captureableloci:
					out3.write('\t'.join(info) + '\n')	
	
				if float(info.count('0')) <= float(0.3*32):				

					out2.write('\t'.join(info) + '\n')
					out.write('\t'.join(info) + '\n')
				else:
					out.write('\t'.join(info) + '\n')

mysignal = [int(x) for x in mysignal[1:]]
myonepiece = [int(x) for x in myonepiece[1:]]

c = [x + y for x,y in zip(mysignal, myonepiece)]
c = [str(x) for x in c]
c.insert(0, 'conkunitzin_signal')
c.insert(0, 'conkunitzin_signal')

info = c

exoncounter += 1
if info.count('0') == 31:
	counter += 1
else:
	if info[0].split('_')[0] in captureableloci:
		out3.write('\t'.join(info) + '\n')

	if float(info.count('0')) <= float(0.3*32):

		out2.write('\t'.join(info) + '\n')
		out.write('\t'.join(info) + '\n')
	else:
		out.write('\t'.join(info) + '\n')












print counter
print exoncounter

	
