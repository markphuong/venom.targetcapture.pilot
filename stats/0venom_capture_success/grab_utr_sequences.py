import os
import sys
from Bio.Seq import translate

myblast = open('utr_transcript.blastoutput', 'r')

blastdict = dict()

alreadyseen = []

for line in myblast:
	info = line.strip().split('\t')
	if info[0] in alreadyseen:
		continue
	else:
		alreadyseen.append(info[0])
		blastdict[info[0]] = info[1]

#print blastdict
#######################


mylist = open('short_terminal_exons.list', 'r')

keeplist = []

for line in mylist:
	info = line.strip().split('\t')
	keeplist.append(info[0])

print len(keeplist)
keeplist = list(set(keeplist))
print len(keeplist)
#print keeplist
#################

myfasta = open('all_venom_utrs.fa','r')

fastadict = dict()

for line in myfasta:
	if ">" in line:


		fastadict[line.strip()[1:]] = next(myfasta).strip()





for item in keeplist:
	info = blastdict[item].split('|')
	#print info
	newheader = blastdict[item]

	seq = fastadict[blastdict[item]]

	start = int(info[-2])
	end = int(info[-1])
	species = info[1]
	out = open(species + '_with_utrs.fa', 'a')

	tseq = translate(seq[start:end])
	if tseq[0] == 'M' and tseq[-1] == '*':
		out.write('>' + newheader + '|' + item.split('|')[0] +  '\n')
		out.write(seq +'\n')
	elif not '*' in tseq:
		print item
		print tseq
		tempseq = translate(seq[start:])
		myindex = tempseq.index('*')

		end = myindex*3+start
					

		out.write('>' + '|'.join(newheader.split('|')[:-1]) + '|' + str(end)+ '|' + item.split('|')[0] + '\n')
		out.write(seq +'\n')
	else:
		print line
		print tseq
	out.close()
			
