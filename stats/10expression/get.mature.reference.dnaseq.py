import os
import sys
from Bio.Seq import translate

##### get dictionary of seq IDs and mature protein sequences

mycono = open('conotoxins_predicted.txt', 'r')

maturedict = dict()

for line in mycono:
	info = line.strip().split('\t')

	maturedict[info[0]] = info[3]

#print maturedict

#################

myuniquemature = open('total_unique_mature_toxins_extractedseq.fa', 'r')

myfamilies = ['A', 'B1', 'B2', 'B4', 'C', 'D', 'DivMKFPLLFISL', 'DivMKLCVVIVLL', 'DivMKLLLTLLLG', 'DivMKVAVVLLVS', 'DivMRFLHFLIVA', 'DivMRFYIGLMAA', 'DivMSKLVILAVL', 'DivMTAKATLLVL', 'DivMTLTFLLVVA', 'E', 'F', 'H', 'I1', 'I2', 'I3', 'I4', 'J', 'K', 'L', 'M', 'MEFRR', 'MEVKM', 'MKFLL', 'MKIVL', 'MMLFM', 'MNCYL', 'MTFYL', 'MTSTL', 'N', 'O1', 'O2', 'O3', 'P', 'S', 'T', 'V', 'Y', 'con-ikot-ikot', 'conkunitzin', 'conodipine', 'conohyal', 'conophysin', 'conoporin']

out = open('unique.mature.toxins.reference.fa', 'w')

for line in myuniquemature:
	if ">" in line:
		ID = line.strip()[1:]

		family = ID.split('|')[2]

		seq = next(myuniquemature).strip()

		myprotein = maturedict[ID]

		if family in myfamilies:

			start = translate(seq).index(myprotein)*3
			end = start + len(myprotein)*3

			out.write(">" + ID + '\n')
			out.write(seq[start:end] + '\n')


