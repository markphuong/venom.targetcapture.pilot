import os
import sys
from numpy import mean

############ load dictionary of exon structure key to functional region

allfamilies = []

regiondict = dict()

myregions = open('functional.region.to.exon.structure.reference', 'r')

#DivMRFLHFLIVA|3pieces|exon3	mature
#D|3pieces|exon1	signal
#T|4pieces|exon2	pre
#T|4pieces|exon3	mature
#T|4pieces|exon1	signal
#T|4pieces|exon4	post


for line in myregions:
	info = line.strip().split('\t')

	family = info[0].split('|')[0]
	exon = info[0].split('|')[2]
	pieces = info[0].split('|')[1]
	allfamilies.append(family)

	regiondict[family + '_' + exon + '_' + pieces] = info[1]

#print regiondict
## {'B2_exon4_4pieces': 'mature', 'conodipine_exon1_2pieces': 'signal', 'S_exon2_3pieces': 'pre', 'V_exon1_3pieces': 'signal', 'K_exon2_3pieces': 'mature', 'MKFLL_exon3_4pieces': 'mature', 'C_exon2_3pieces': 'pre', 'DivMRFLHFLIVA_exon3_3pieces': 'mature', 'M_exon1_3pieces': 'signal', 'con-ikot-ikot_exon4_4pieces': 'post', 'DivMKVAVVLLVS_exon3_3pieces': 'post', 'M_exon3_3pieces': 'mature', 'MNCYL_exon1_4pieces': 'signal', 'I1_exon2_3pieces': 'pre', 'T_exon3_4pieces': 'mature', 'V_exon3_3pieces': 'mature', 'DivMKLCVVIVLL_exon2_4pieces': 'pre', 'conophysin_exon2_3pieces': 'mature', 'J_exon1_1pieces': 'onepiece', 'MEFRR_exon4_4pieces': 'post', 'I4_exon1_3pieces': 'signal', 'O3_exon2_3pieces': 'pre', 'V_exon2_3pieces': 'pre', 'DivMKLLLTLLLG_exon6_6pieces': 'post', 'conoporin_exon2_4pieces': 'pre', 'H_exon1_3pieces': 'signal', 'D_exon2_3pieces': 'pre', 'conophysin_exon3_3pieces': 'post', 'DivMKLCVVIVLL_exon1_4pieces': 'signal', 'MNCYL_exon4_4pieces': 'post', 'conkunitzin_exon1_3pieces': 'signal', 'C_exon1_3pieces': 'signal', 'conoporin_exon4_4pieces': 'post', 'I2_exon1_3pieces': 'signal', 'DivMKVAVVLLVS_exon2_3pieces': 'mature', 'B4_exon1_1pieces': 'onepiece', 'I4_exon2_3pieces': 'mature', 'F_exon1_3pieces': 'signal', 'O1_exon1_3pieces': 'signal', 'E_exon1_3pieces': 'signal', 'I2_exon3_3pieces': 'post', 'I3_exon3_3pieces': 'mature', 'Y_exon2_3pieces': 'pre', 'conkunitzin_exon2_3pieces': 'mature', 'DivMTLTFLLVVA_exon3_3pieces': 'mature', 'P_exon2_4pieces': 'pre', 'M_exon2_3pieces': 'pre', 'con-ikot-ikot_exon2_4pieces': 'pre', 'O2_exon3_3pieces': 'mature', 'DivMKLLLTLLLG_exon1_6pieces': 'signal', 'L_exon1_3pieces': 'signal', 'DivMRFYIGLMAA_exon1_5pieces': 'signal', 'N_exon2_3pieces': 'pre', 'I1_exon3_3pieces': 'mature', 'conohyal_exon4_5pieces': 'pre', 'MMLFM_exon1_4pieces': 'signal', 'DivMKFPLLFISL_exon4_4pieces': 'post', 'DivMKLCVVIVLL_exon4_4pieces': 'post', 'MTFYL_exon1_4pieces': 'signal', 'D_exon1_3pieces': 'signal', 'F_exon2_3pieces': 'mature', 'A_exon2_2pieces': 'mature', 'conkunitzin_exon3_3pieces': 'post', 'DivMTLTFLLVVA_exon2_3pieces': 'pre', 'F_exon3_3pieces': 'post', 'MMLFM_exon4_4pieces': 'post', 'O3_exon3_3pieces': 'mature', 'DivMKFPLLFISL_exon1_4pieces': 'signal', 'MEFRR_exon3_4pieces': 'mature', 'N_exon3_3pieces': 'mature', 'DivMKVAVVLLVS_exon1_3pieces': 'signal', 'O1_exon3_3pieces': 'mature', 'MTFYL_exon3_4pieces': 'mature', 'con-ikot-ikot_exon1_4pieces': 'signal', 'P_exon4_4pieces': 'post', 'I2_exon2_3pieces': 'mature', 'S_exon1_3pieces': 'signal', 'K_exon3_3pieces': 'post', 'Y_exon3_3pieces': 'mature', 'T_exon2_4pieces': 'pre', 'K_exon1_3pieces': 'signal', 'MEFRR_exon2_4pieces': 'pre', 'C_exon3_3pieces': 'mature', 'T_exon1_4pieces': 'signal', 'H_exon3_3pieces': 'mature', 'P_exon3_4pieces': 'mature', 'I4_exon3_3pieces': 'post', 'MNCYL_exon3_4pieces': 'mature', 'D_exon3_3pieces': 'mature', 'H_exon2_3pieces': 'pre', 'conohyal_exon1_5pieces': 'signal', 'MKFLL_exon1_4pieces': 'signal', 'con-ikot-ikot_exon3_4pieces': 'mature', 'T_exon4_4pieces': 'post', 'MEFRR_exon1_4pieces': 'signal', 'A_exon1_2pieces': 'signal', 'DivMKFPLLFISL_exon3_4pieces': 'mature', 'Y_exon1_3pieces': 'signal', 'I3_exon1_3pieces': 'signal', 'B1_exon1_1pieces': 'onepiece', 'conoporin_exon3_4pieces': 'mature', 'B2_exon1_4pieces': 'signal', 'conodipine_exon2_2pieces': 'mature', 'L_exon3_3pieces': 'mature', 'O2_exon1_3pieces': 'signal', 'conohyal_exon5_5pieces': 'mature', 'O2_exon2_3pieces': 'pre', 'I3_exon2_3pieces': 'pre', 'L_exon2_3pieces': 'pre', 'MMLFM_exon3_4pieces': 'pre', 'E_exon2_3pieces': 'mature', 'MEVKM_exon2_2pieces': 'mature', 'O3_exon1_3pieces': 'signal', 'O1_exon2_3pieces': 'pre', 'I1_exon1_3pieces': 'signal', 'conophysin_exon1_3pieces': 'signal', 'DivMKLCVVIVLL_exon3_4pieces': 'mature', 'MMLFM_exon2_4pieces': 'mature', 'N_exon1_3pieces': 'signal', 'S_exon3_3pieces': 'mature', 'conoporin_exon1_4pieces': 'signal', 'P_exon1_4pieces': 'signal'}



############### count num mature per family

myunique = open('unique.mature.toxins.reference.fa', 'r')

# >Vi6.7|virgo|O3|8809.16182573

uniquedict = dict() # dictionary for a specific species counting the number of unique mature toxins per family
lengthdict = dict() # dictionary for each unique mature toxin for that species, save the length of that toxin

for line in myunique:
	if ">" in line:
		info = line.strip()[1:].split('|')

		species = info[1]
		family = info[2]

		seq = next(myunique).strip()


		if species == sys.argv[2]:
			lengthdict[line.strip()[1:]] = len(seq)
			if family in uniquedict:
				uniquedict[family] += 1
			else:
				uniquedict[family] = 1


print uniquedict #### {'A': 3, 'MEFRR': 3, 'E': 1, 'conodipine': 3, 'F': 1, 'MKFLL': 1, 'conophysin': 3, 'I2': 10, 'M': 4, 'N': 4, 'con-ikot-ikot': 1, 'T': 4, 'conkunitzin': 1, 'V': 2, 'Y': 2, 'O3': 1, 'O2': 7, 'O1': 19, 'B1': 1}


##################### store dictionary of mature exons, estimated by the majority consensus mature exon per family

myfasta = open(sys.argv[3], 'r')


exonnamedict = dict() ##dictionary containing all 'mature' exons

for line in myfasta:
	if ">" in line:
		info = line.strip()[1:].split('|')

		family = info[1]

		region = info[-1]

		if region =='mature' or region =='onepiece':


			if family in exonnamedict:

				exonnamedict[family].append(info[0])

			else:
				exonnamedict[family] = [info[0]]


print exonnamedict #{'MEFRR': ['seed_4946_90_1'], 'O3': ['seed_2577_90_1', 'seed_4123_90_1'], 'O2': ['seed_3478_90_1', 'seed_3481_90_1', 'seed_3952_90_1', 'seed_3953_90_1', 'seed_3955_90_1', 'seed_3957_90_1', 'seed_4153_90_1', 'seed_4400_90_1', 'seed_4442_90_1', 'seed_4455_90_1', 'seed_4457_90_1', 'seed_4618_92_1', 'seed_4716_90_1', 'seed_4854_90_1', 'seed_4873_90_1', 'seed_4960_90_1', 'seed_4961_92_1', 'seed_4962_90_1', 'seed_5415_90_1', 'seed_5619_90_1', 'seed_6257_90_1', 'seed_6258_90_1', 'seed_730_98_1'], 'O1': ['seed_108_90_1', 'seed_111_90_1', 'seed_116_90_1', 'seed_136_90_1', 'seed_175_94_1', 'seed_200_90_1', 'seed_201_90_1', 'seed_221_90_1', 'seed_222_90_1', 'seed_247_90_1', 'seed_249_94_1', 'seed_250_90_1', 'seed_266_90_1', 'seed_269_90_1', 'seed_270_90_1', 'seed_271_92_1', 'seed_277_90_1', 'seed_281_94_1', 'seed_2829_92_1', 'seed_305_90_1', 'seed_314_90_1', 'seed_315_90_1', 'seed_318_92_1', 'seed_321_90_1', 'seed_323_90_1', 'seed_3389_90_1', 'seed_3399_90_1', 'seed_3726_90_1', 'seed_4031_90_1', 'seed_4040_90_1', 'seed_4201_90_1', 'seed_4203_90_1', 'seed_428_90_1', 'seed_429_90_1', 'seed_4475_90_1', 'seed_4583_90_1', 'seed_4892_90_1', 'seed_4929_90_1', 'seed_4931_90_1', 'seed_5133_90_1', 'seed_5317_90_1', 'seed_67_90_1', 'seed_68_90_1', 'seed_69_90_1', 'seed_70_90_1', 'seed_72_90_1', 'seed_916_90_1', 'seed_933_94_1'], 'I1': ['seed_4272_90_1', 'seed_824_90_1'], 'I2': ['seed_2357_90_1', 'seed_2358_90_1', 'seed_2359_90_1', 'seed_2362_90_1', 'seed_2787_92_1', 'seed_2788_90_1', 'seed_3902_90_1', 'seed_4336_92_1', 'seed_4483_90_1', 'seed_559_90_1'], 'conophysin': ['seed_4267_90_1', 'seed_5046_98_1', 'seed_987_90_1'], 'conodipine': ['seed_3617_90_1', 'seed_3620_90_1', 'seed_4046_90_1'], 'A': ['seed_1037_92_1', 'seed_1038_90_1', 'seed_2546_92_1', 'seed_2548_90_1', 'seed_3791_90_1', 'seed_4888_90_1', 'seed_4889_90_1'], 'C': ['seed_4750_90_1'], 'E': ['seed_676_90_1'], 'H': ['seed_5544_92_1', 'seed_5545_96_1'], 'J': ['seed_3546_94_1'], 'M': ['seed_2237_90_1', 'seed_2240_90_1', 'seed_2253_90_1', 'seed_2255_90_1', 'seed_4230_92_1', 'seed_4529_90_1', 'seed_4546_98_1', 'seed_4548_90_1', 'seed_4728_92_1', 'seed_5077_90_1', 'seed_5095_90_1', 'seed_5097_90_1', 'seed_690_90_1', 'seed_691_90_1', 'seed_692_90_1', 'seed_693_90_1'], 'L': ['seed_4964_90_1'], 'N': ['seed_4429_90_1', 'seed_893_90_1', 'seed_896_90_1'], 'T': ['seed_1192_90_1', 'seed_1193_90_1', 'seed_5591_90_1', 'seed_5648_90_1', 'seed_5649_90_1', 'seed_5650_90_1'], 'DivMKVAVVLLVS': ['seed_2636_90_1'], 'V': ['seed_4224_98_1', 'seed_5035_90_1', 'seed_5037_90_1'], 'Y': ['seed_3995_90_1', 'seed_4684_94_1', 'seed_4685_90_1'], 'conoporin': ['seed_1015_90_1', 'seed_3970_90_1'], 'B4': ['seed_4550_90_1'], 'B1': ['seed_3464_90_1'], 'B2': ['seed_4537_92_1'], 'conkunitzin': ['seed_4942_98_1', 'seed_5437_90_1']}

#########################################
myblast = open(sys.argv[1], 'r')

#Vi6.7|virgo|O3|8809.16182573	seed_2577_90_1|O3|exon3|3pieces|457|553|blastx|onecopy	100.00	90	0	0	7	96	1	90	1e-44	167
#Vi1.6|virgo|A|61367.0842105	seed_2546_92_1|A|exon2|2pieces|42|159|blastx|hap1	100.00	78	0	0	1	78	34	111	4e-38	145
#Vi1.6|virgo|A|61367.0842105	seed_2546_92_1|A|exon2|2pieces|42|159|blastx|hap2	98.72	78	1	0	1	78	34	111	2e-36	139
#Vi1.6|virgo|A|61367.0842105	seed_2548_90_1|A|exon2|2pieces|34|151|blastx|onecopy	96.15	78	3	0	1	78	34	111	4e-33	128

expressedlist = [] #list of unique mature toxins that were recovered in the genome
myexondict = dict() #dictionary of exons that are expressed that were recovered in genome


#for sequences below 30, accept an evalue higher than 1e-10 but lower than 1-e3
#if the sequence covered at least 70% of the sequence at > 95% identity
#or matched an exon identified as the majority consensus 'mature' exon
# save that seed name and also the unique mature toxin ID

for line in myblast:
	info = line.strip().split('\t')
	mylength = int(info[7]) - (int(info[6])-1)

	myfamily = info[1].split('|')[1]

	myevalue = float(info[-2])



	if info[0].split('|')[1] == sys.argv[2]:
		if myevalue < 1e-10 or lengthdict[info[0]] < 30:
			if float(mylength)/lengthdict[info[0]] >= 0.8:
				expressedlist.append(info[0])
				if myfamily in myexondict:
					myexondict[myfamily].append(info[1].split('|')[0])
				else:
					myexondict[myfamily] = [info[1].split('|')[0]]

			elif myfamily in exonnamedict and info[1].split('|')[0] in exonnamedict[myfamily]:
				expressedlist.append(info[0])
				if myfamily in myexondict:
					myexondict[myfamily].append(info[1].split('|')[0])
				else:
					myexondict[myfamily] = [info[1].split('|')[0]]

			else:
				print line

			



#print expressedlist  #['Vi6.7|virgo|O3|8809.16182573', 'Vi1.6|virgo|A|61367.0842105', 'Vi1.6|virgo|A|61367.0842105', 'Vi1.6|virgo|A|61367.0842105', 'Contryphan-Vi|virgo|O2|19234.9481865', 'Vi6.1|virgo|O1|44528.8008299', 'Vi6.1|virgo|O1|44528.8008299', 'Vi6.1|virgo|O1|44528.8008299', 'Vi11.5|virgo|I2|16928.5794393', 'ViTx|virgo|I2|57547.1902439', 'ViTx|virgo|I2|57547.1902439', 'ViXVA|virgo|V|32392.9585062', 'ViVB|virgo|T|27930.9944751', 'ViVA|virgo|T|45837.7348066', 'Vi11.2|virgo|I2|18714.7336449', 'Vi11.2|virgo|I2|18714.7336449', 'Vi6.9|virgo|O1|32814.8340249', 'Vi6.9|virgo|O1|32814.8340249', 'Vi6.9|virgo|O1|32814.8340249', 'Vi_A_3|virgo|A|25777.2072539', 'Vi_A_3|virgo|A|25777.2072539', 'Vi_A_5|virgo|A|14634.9473684', 'Vi_A_5|virgo|A|14634.9473684', 'Vi_B1_1|virgo|B1|129.525568182', 'Vi_E_1|virgo|E|2888.27413127', 'Vi_I2_5|virgo|I2|1089.53365385', 'Vi_I2_6|virgo|I2|1173.7014218', 'Vi_I2_7|virgo|I2|23839.8365385', 'Vi_I2_7|virgo|I2|23839.8365385', 'Vi_I2_8|virgo|I2|12565.9711538', 'Vi_I2_8|virgo|I2|12565.9711538', 'Vi_I2_9|virgo|I2|426.931818182', 'Vi_I2_12|virgo|I2|4828.06122449', 'Vi_I2_12|virgo|I2|4828.06122449', 'Vi_I2_13|virgo|I2|9611.57476636', 'Vi_I2_13|virgo|I2|9611.57476636', 'Vi_M_2|virgo|M|45920.056872', 'Vi_M_2|virgo|M|45920.056872', 'Vi_M_2|virgo|M|45920.056872', 'Vi_M_2|virgo|M|45920.056872', 'Vi_M_3|virgo|M|5838.23834197', 'Vi_M_3|virgo|M|5838.23834197', 'Vi_M_6|virgo|M|7787.80237154', 'Vi_M_8|virgo|M|2768.60576923', 'Vi_MEFRR_1|virgo|MEFRR|170.238866397', 'Vi_MEFRR_1|virgo|MEFRR|170.238866397', 'Vi_MEFRR_2|virgo|MEFRR|657.141700405', 'Vi_MEFRR_2|virgo|MEFRR|657.141700405', 'Vi_N_1|virgo|N|4625.92123288', 'Vi_O1_7|virgo|O1|800.082987552', 'Vi_O1_8|virgo|O1|10595.5491803', 'Vi_O1_8|virgo|O1|10595.5491803', 'Vi_O1_8|virgo|O1|10595.5491803', 'Vi_O1_8|virgo|O1|10595.5491803', 'Vi_O1_9|virgo|O1|8.18852459016', 'Vi_O1_10|virgo|O1|58976.7681818', 'Vi_O1_11|virgo|O1|1148.11206897', 'Vi_O1_11|virgo|O1|1148.11206897', 'Vi_O1_11|virgo|O1|1148.11206897', 'Vi_O1_11|virgo|O1|1148.11206897', 'Vi_O1_11|virgo|O1|1148.11206897', 'Vi_O1_11|virgo|O1|1148.11206897', 'Vi_O1_12|virgo|O1|3740.80603448', 'Vi_O1_12|virgo|O1|3740.80603448', 'Vi_O1_12|virgo|O1|3740.80603448', 'Vi_O1_12|virgo|O1|3740.80603448', 'Vi_O1_12|virgo|O1|3740.80603448', 'Vi_O1_12|virgo|O1|3740.80603448', 'Vi_O1_12|virgo|O1|3740.80603448', 'Vi_O1_13|virgo|O1|1081.96982759', 'Vi_O1_13|virgo|O1|1081.96982759', 'Vi_O1_13|virgo|O1|1081.96982759', 'Vi_O1_13|virgo|O1|1081.96982759', 'Vi_O1_13|virgo|O1|1081.96982759', 'Vi_O1_13|virgo|O1|1081.96982759', 'Vi_O1_14|virgo|O1|1289.78448276', 'Vi_O1_14|virgo|O1|1289.78448276', 'Vi_O1_14|virgo|O1|1289.78448276', 'Vi_O1_14|virgo|O1|1289.78448276', 'Vi_O1_14|virgo|O1|1289.78448276', 'Vi_O1_14|virgo|O1|1289.78448276', 'Vi_O1_15|virgo|O1|4928.57758621', 'Vi_O1_15|virgo|O1|4928.57758621', 'Vi_O1_16|virgo|O1|2051.6846473', 'Vi_O1_16|virgo|O1|2051.6846473', 'Vi_O1_16|virgo|O1|2051.6846473', 'Vi_O1_16|virgo|O1|2051.6846473', 'Vi_O1_18|virgo|O1|5041.22689076', 'Vi_O1_18|virgo|O1|5041.22689076', 'Vi_O1_19|virgo|O1|11460.3817427', 'Vi_O1_19|virgo|O1|11460.3817427', 'Vi_O1_19|virgo|O1|11460.3817427', 'Vi_O1_19|virgo|O1|11460.3817427', 'Vi_O1_21|virgo|O1|9584.08196721', 'Vi_O1_21|virgo|O1|9584.08196721', 'Vi_O1_21|virgo|O1|9584.08196721', 'Vi_O1_21|virgo|O1|9584.08196721', 'Vi_O1_21|virgo|O1|9584.08196721', 'Vi_O1_21|virgo|O1|9584.08196721', 'Vi_O1_23|virgo|O1|10455.3401639', 'Vi_O1_23|virgo|O1|10455.3401639', 'Vi_O1_23|virgo|O1|10455.3401639', 'Vi_O1_23|virgo|O1|10455.3401639', 'Vi_O1_23|virgo|O1|10455.3401639', 'Vi_O1_23|virgo|O1|10455.3401639', 'Vi_O1_26|virgo|O1|31482.8049793', 'Vi_O1_26|virgo|O1|31482.8049793', 'Vi_O1_26|virgo|O1|31482.8049793', 'Vi_O1_27|virgo|O1|33517.6434426', 'Vi_O1_27|virgo|O1|33517.6434426', 'Vi_O1_27|virgo|O1|33517.6434426', 'Vi_O1_30|virgo|O1|672.760617761', 'Vi_O1_30|virgo|O1|672.760617761', 'Vi_O2_2|virgo|O2|11855.7433628', 'Vi_O2_2|virgo|O2|11855.7433628', 'Vi_O2_6|virgo|O2|1316.86740331', 'Vi_O2_8|virgo|O2|16313.8663968', 'Vi_O2_8|virgo|O2|16313.8663968', 'Vi_O2_9|virgo|O2|8239.02112676', 'Vi_O2_10|virgo|O2|30653.973262', 'Vi_O2_11|virgo|O2|5064.01793722', 'Vi_O2_11|virgo|O2|5064.01793722', 'Vi_T_7|virgo|T|53518.0829016', 'Vi_T_8|virgo|T|2403.60427807', 'Vi_T_8|virgo|T|2403.60427807', 'Vi_V_2|virgo|V|1100.02521008', 'Vi_Y_1|virgo|Y|3766.64159292', 'Vi_Y_1|virgo|Y|3766.64159292', 'Vi_Y_1|virgo|Y|3766.64159292', 'Vi_Y_2|virgo|Y|11252.2345133', 'Vi_Y_2|virgo|Y|11252.2345133', 'Vi_Y_2|virgo|Y|11252.2345133', 'Vi_conkunitzin_1|virgo|conkunitzin|5729.81081081', 'Vi_conodipine_1|virgo|conodipine|589.756007394', 'Vi_conodipine_1|virgo|conodipine|589.756007394', 'Vi_conodipine_2|virgo|conodipine|44.3909090909', 'Vi_conodipine_2|virgo|conodipine|44.3909090909', 'Vi_conodipine_3|virgo|conodipine|49.9363636364', 'Vi_conodipine_3|virgo|conodipine|49.9363636364', 'Vi_conophysin_1|virgo|conophysin|19078.739011', 'Vi_conophysin_1|virgo|conophysin|19078.739011', 'Vi_conophysin_2|virgo|conophysin|12832.6428571', 'Vi_conophysin_2|virgo|conophysin|12832.6428571', 'Vi_conophysin_3|virgo|conophysin|7673.99450549', 'Vi_conophysin_3|virgo|conophysin|7673.99450549']

capturedict = dict()

for item in set(expressedlist):
	family = item.split('|')[2]

	if family in capturedict:
		capturedict[family] += 1
	else:
		capturedict[family] = 1

#print capturedict {'A': 3, 'MEFRR': 2, 'E': 1, 'conophysin': 3, 'I2': 10, 'M': 4, 'N': 1, 'conkunitzin': 1, 'T': 4, 'conodipine': 3, 'V': 2, 'Y': 2, 'O3': 1, 'O2': 7, 'O1': 19, 'B1': 1}

# if you recovered at least 90% of the sequences of a family, perform % genes expressed calculation


out = open('expressed.stats', 'a')

output = ['species']

for family in sorted(set(allfamilies)):
	output.append(family)

#out.write('\t'.join(output) + '\n')


#print myexondict['DivMRFYIGLMAA']
#print exonnamedict['DivMRFYIGLMAA']

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

averagethis = []

output = [sys.argv[2]]
for family in sorted(set(allfamilies)):

	if family in capturedict:
		if float(capturedict[family])/float(uniquedict[family]) >= 0.9:
			for seqID in set(myexondict[family]):
				if family in exonnamedict:
					exonnamedict[family].append(seqID)
				else:
					exonnamedict[family] = [seqID]



			averagethis.append(float(len(list(set(myexondict[family]))))/len(list(set(exonnamedict[family]))))
			output.append(str(len(list(set(myexondict[family])))) + '/' +str(len(list(set(exonnamedict[family]))))+' ('+'{0:.0%}'.format(float(len(list(set(myexondict[family]))))/len(list(set(exonnamedict[family])))) + ')')
		else:
			output.append('-')

	elif not family in uniquedict and family in exonnamedict and family in captureableloci:
		myexondict[family] = []
		averagethis.append(float(len(list(set(myexondict[family]))))/len(list(set(exonnamedict[family]))))
		output.append(str(len(list(set(myexondict[family])))) + '/' +str(len(list(set(exonnamedict[family]))))+' ('+'{0:.0%}'.format(float(len(list(set(myexondict[family]))))/len(list(set(exonnamedict[family])))) + ')')

	else:
		output.append('-')

out.write('\t'.join(output) + '\n')

out2 = open('avg.expressed', 'a')

out2.write(sys.argv[2] + '\t'+ str(mean(averagethis)) + '\n')



















