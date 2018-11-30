import pickle
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy


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


#|-------------------|#
#|--   Main Loop   --|#
#|-------------------|#

# exp = {
# 	"1":{"pool":set(), "wells": {"1-1":(set(), []), "1-2":(set(), []), "2-1":(set(), []), "2-2":(set(), [])}},
# 	"2":{"pool":set(), "wells": {"1-1":(set(), []), "1-2":(set(), []), "2-1":(set(), []), "2-2":(set(), [])}},
# 	"3":{"pool":set(), "wells": {"1-1":(set(), []), "1-2":(set(), []), "2-1":(set(), []), "2-2":(set(), [])}},
# 	"4":{"pool":set(), "wells": {"1-1":(set(), []), "1-2":(set(), []), "2-1":(set(), []), "2-2":(set(), [])}}
# }

LT_dict = {
	"pool":set(),
	"wells":{
			"well_1":(set(), []),
			"well_2":(set(), []),
			"well_3":(set(), []),
			"well_4":(set(), []),
			"well_5":(set(), []),
			"well_6":(set(), []),
			"well_7":(set(), []),
			"well_8":(set(), [])
	}
}

for key in ins_dict:
	for c in ins_dict[key]:
		for w in ins_dict[key][c]:
			if ins_dict[key][c][w] >= 2 and len(key) in range(5,16):
				LT_dict["pool"].add(key)
				LT_dict["wells"][w][0].add(key)


# for key in umi_dict:
# 	exp[umi_dict[key]["well"][0]]["pool"].add(umi_dict[key]["ins"])
# 	exp[umi_dict[key]["well"][0]]["wells"][umi_dict[key]["well"][2:]][0].add(umi_dict[key]["ins"])

# exp1_counter = 0
# exp2_counter = 0
# exp3_counter = 0
# exp4_counter = 0

# for key in umi_dict:
# 	if umi_dict[key]["well"][0] == '1':
# 		exp1_counter += 1
# 	elif umi_dict[key]["well"][0] == '2':
# 		exp2_counter += 1
# 	elif umi_dict[key]["well"][0] == '3':
# 		exp3_counter += 1
# 	elif umi_dict[key]["well"][0] == '4':
# 		exp4_counter += 1
		
dist_array = pd.DataFrame(columns=[x for x in LT_dict["wells"]], index=[x for x in LT_dict["wells"]])

for ins in LT_dict["pool"]:
	for well in LT_dict["wells"]:
		if ins in LT_dict["wells"][well][0]:
			LT_dict["wells"][well][1].append(1)
		else:
			LT_dict["wells"][well][1].append(0)

for well in LT_dict["wells"]:
	print(well)
	print(len(LT_dict["wells"][well][0]))
	print(len(LT_dict["wells"][well][1]))
print(len(LT_dict["pool"]))
well_list = [x for x in LT_dict["wells"]]


## Jaccard
for x, y in itertools.combinations(well_list, 2):
	_11 = sum_11(LT_dict["wells"][x][1], LT_dict["wells"][y][1])
	_01_10 = sum_01_10(LT_dict["wells"][x][1], LT_dict["wells"][y][1])
	dist_array.at[x, y] = (_01_10)/(_11 + _01_10)
	dist_array.at[y, x] = (_01_10)/(_11 + _01_10)
	dist_array.at[x, x] = 0
	dist_array.at[y, y] = 0
print(dist_array)

#Kulczynski-2
# for x, y in itertools.combinations(well_list, 2):
# 	_11 = sum_11(LT_dict["wells"][x][1], LT_dict["wells"][y][1])
# 	_01_10 = sum_01_10(LT_dict["wells"][x][1], LT_dict["wells"][y][1])
# 	_1x = sum_1(LT_dict["wells"][x][1])
# 	_1y = sum_1(LT_dict["wells"][y][1])
# 	dist_array.at[x, y] = .5*((_11/(_11+_1x)) + (_11/(_11+_1y)))
# 	dist_array.at[y, x] = .5*((_11/(_11+_1x)) + (_11/(_11+_1y)))
# 	dist_array.at[x, x] = 1
# 	dist_array.at[y, y] = 1
# print(dist_array)

z = hierarchy.linkage(dist_array, 'average')#, optimal_ordering=True)
plt.figure()

dn = hierarchy.dendrogram(z)
plt.show()

# for exp_num in exp:
# 	dist_array = pd.DataFrame(columns=[[x for x in exp[exp_num]["wells"]]], index=[[x for x in exp[exp_num]["wells"]]])
# 	for ins in exp[exp_num]["pool"]:
# 		for well in exp[exp_num]["wells"]:
# 			if ins in exp[exp_num]["wells"][well][0]:
# 				exp[exp_num]["wells"][well][1].append(1)
# 			else:
# 				exp[exp_num]["wells"][well][1].append(0)	
# 	# print("Pool length for this experiment is: "+str(len(exp[exp_num]["pool"])))
# 	well_list = [x for x in exp[exp_num]["wells"]]
# 	for x, y in itertools.combinations(well_list, 2):
# 		a = len(exp[exp_num]["wells"][x][0])
# 		b = len(exp[exp_num]["wells"][y][0])
# 		# lUnion = sumUnion(exp[exp_num]["wells"][x][1], exp[exp_num]["wells"][y][1])
# 		# lInter = sumInter(exp[exp_num]["wells"][x][1], exp[exp_num]["wells"][y][1])
# 		# dist_array.at[x, y] = (lUnion/lInter)
# 		# dist_array.at[y, x] = (lUnion/lInter)
# 		dist_array.at[x, y] = (matchScore(exp[exp_num]["wells"][x][0], exp[exp_num]["wells"][y][0]))/(a+b)
# 		dist_array.at[y, x] = (matchScore(exp[exp_num]["wells"][x][0], exp[exp_num]["wells"][y][0]))/(a+b)
# 		dist_array.at[x, x] = (matchScore(exp[exp_num]["wells"][x][0], exp[exp_num]["wells"][x][0]))/(a+b)
# 		dist_array.at[y, y] = (matchScore(exp[exp_num]["wells"][y][0], exp[exp_num]["wells"][y][0]))/(a+b)
# 		# print(f"Run {exp_num}: "+str(lInter) + f" for {x} ({a}) and {y} ({b}) and they had {lUnion} ins in common")
# 		#print(str(sumUnion(exp[key]["wells"][x][1], exp[key]["wells"][y][1])) + f"for {x} and {y}")
# 	print(f"distance array for exp num {exp_num}:")
# 	print(dist_array)