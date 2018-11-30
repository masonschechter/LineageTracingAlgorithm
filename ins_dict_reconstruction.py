import pickle
import itertools
import pandas as pd

#|-------------------|#
#|-- FUNCTION DEFS --|#
#|-------------------|#
def sum_11(l1,l2):
	num = 0
	for i in range(len(l1)):
		if (l1[i], l2[i]) == (1, 1):
			num += 1
	return num

def sum_01_10(l1,l2):
	num = 0
	for i in range(len(l1)):
		if ((l1[i], l2[i]) == (0, 1) or ((l1[i], l2[i]) == (1, 0))):
			num += 1
	return num

def sum_1(l1):
	num = 0
	for i in range(len(l1)):
		if l1[i] == 1:
			num += 1
	return num

def matchScore(l1,l2):
	score = 0
	for x in l1:
		for y in l2:
			for i in range(len(x)):
				if i < len(y) and x[i] == y[i]:
					score += 1
				else:
					break
	return score

#|-------------------|#
#|-- Pickle Loading--|#
#|-------------------|#
with open('384_well_LT_ins_dict.pkl', 'rb') as file:
	ins_dict = pickle.load(file)

# ins_dict = {
	# insertion:{
# 		"seqs" : {
#			"well" : []
#		}
# 		"umis" : {
#			"well" : []
#		}
# 		"counts": {
#			"well" : int()
#		}
# 	}
# }

#|-------------------|#
#|--   Main Loop   --|#
#|-------------------|#

winners = {}

for key in ins_dict:
	unique = 0
	if len(ins_dict[key]["umis"]) == 2:
		for well in ins_dict[key]["umis"]:
			unique += len(ins_dict[key]["umis"][well])
			winners[key] = unique
winners_sorted = sorted(winners)
for x in winners_sorted:
	print(f"{x}: {winners[x]}")
	# for well in ins_dict[key]["umis"]:
		# a = len(ins_dict[key]["umis"][well])	
		# print(f"{a} umis in {well} for {key}")
		# unique += len(ins_dict[key]["umis"][well])
		# if unique >= 3:
			# print(f"{unique} unique occurences of {key}")