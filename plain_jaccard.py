import pickle
import prefixTree as pTree
import itertools
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist, squareform

with open('384_well_LT_ins_dict.pkl', 'rb') as file:
	ins_dict = pickle.load(file)

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

wells = ['well_1', 'well_2', 'well_3', 'well_4', 'well_5', 'well_6', 'well_7', 'well_8']

# well_dict = {
# 	"well": {
# 		"ins": {
# 			"umi_count": int()
# 			"ins_count": int()
# 		}
# 	}
# }
LT_dict = {
	"pool":set(),
	"wells":{
			"well_1":[set(), []],
			"well_2":[set(), []],
			"well_3":[set(), []],
			"well_4":[set(), []],
			"well_5":[set(), []],
			"well_6":[set(), []],
			"well_7":[set(), []],
			"well_8":[set(), []]
	}
}

for ins in ins_dict:
	if not ins == 'ROOT':
		if len(ins) in range(8,15):
			for well in ins_dict[ins]["counts"]:
				if ins_dict[ins]["counts"][well] >= 50:
					LT_dict["pool"].add(ins)
					LT_dict["wells"][well][0].add(ins)

dist_array = pd.DataFrame(columns=[x for x in LT_dict["wells"]], index=[x for x in LT_dict["wells"]])


LT_dict["pool"] = sorted(LT_dict["pool"])

for well in LT_dict["wells"]:
	LT_dict["wells"][well][0] = sorted(LT_dict["wells"][well][0])
	print(well)
	print({len(LT_dict["wells"][well][0])})



for ins in LT_dict["pool"]:
	for well in LT_dict["wells"]:
		if ins in LT_dict["wells"][well][0]:
			LT_dict["wells"][well][1].append(1)
		else:
			LT_dict["wells"][well][1].append(0)

for well in LT_dict["wells"]:
	print(len(LT_dict["wells"][well][1]))




for x, y in itertools.combinations(wells, 2):
	_11 = sum_11(LT_dict["wells"][x][1], LT_dict["wells"][y][1])
	_01_10 = sum_01_10(LT_dict["wells"][x][1], LT_dict["wells"][y][1])
	dist_array.at[x, y] = 1-((_01_10)/(_11 + _01_10))
	dist_array.at[y, x] = 1-((_01_10)/(_11 + _01_10))
	dist_array.at[x, x] = 1
	dist_array.at[y, y] = 1
print(dist_array)

dist_array.to_csv("plain_jaccard_length8-15.csv")



z = hierarchy.linkage(dist_array, 'average')#, optimal_ordering=True)
plt.figure()

dn = hierarchy.dendrogram(z)
plt.show()








