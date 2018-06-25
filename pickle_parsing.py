import pickle
import itertools
import pandas as pd


#|-------------------|#
#|-- FUNCTION DEFS --|#
#|-------------------|#
def sumUnion(l1,l2):
	num = 0
	for i in range(len(l1)):
		if (l1[i], l2[i]) == (1, 1):
			num += 1
	return num

def sumInter(l1,l2):
	num = 0
	for i in range(len(l1)):
		if ((l1[i], l2[i]) == (0, 1) or ((l1[i], l2[i]) == (1, 0))):
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
with open('umi_pickle.txt', 'rb') as file:
	umi_dict = pickle.load(file)


#|-------------------|#
#|--   Main Loop   --|#
#|-------------------|#

exp = {
	"1":{"pool":set(), "wells": {"1-1":(set(), []), "1-2":(set(), []), "2-1":(set(), []), "2-2":(set(), [])}},
	"2":{"pool":set(), "wells": {"1-1":(set(), []), "1-2":(set(), []), "2-1":(set(), []), "2-2":(set(), [])}},
	"3":{"pool":set(), "wells": {"1-1":(set(), []), "1-2":(set(), []), "2-1":(set(), []), "2-2":(set(), [])}},
	"4":{"pool":set(), "wells": {"1-1":(set(), []), "1-2":(set(), []), "2-1":(set(), []), "2-2":(set(), [])}}
}


for key in umi_dict:
	exp[umi_dict[key]["well"][0]]["pool"].add(umi_dict[key]["ins"])
	exp[umi_dict[key]["well"][0]]["wells"][umi_dict[key]["well"][2:]][0].add(umi_dict[key]["ins"])

for exp_num in exp:
	dist_array = pd.DataFrame(columns=[[x for x in exp[exp_num]["wells"]]], index=[[x for x in exp[exp_num]["wells"]]])
	for ins in exp[exp_num]["pool"]:
		for well in exp[exp_num]["wells"]:
			if ins in exp[exp_num]["wells"][well][0]:
				exp[exp_num]["wells"][well][1].append(1)
			else:
				exp[exp_num]["wells"][well][1].append(0)	
	# print("Pool length for this experiment is: "+str(len(exp[exp_num]["pool"])))
	well_list = [x for x in exp[exp_num]["wells"]]
	for x, y in itertools.combinations(well_list, 2):
		a = len(exp[exp_num]["wells"][x][0])
		b = len(exp[exp_num]["wells"][y][0])
		# lUnion = sumUnion(exp[exp_num]["wells"][x][1], exp[exp_num]["wells"][y][1])
		# lInter = sumInter(exp[exp_num]["wells"][x][1], exp[exp_num]["wells"][y][1])
		# dist_array.at[x, y] = (lUnion/lInter)
		# dist_array.at[y, x] = (lUnion/lInter)
		dist_array.at[x, y] = (matchScore(exp[exp_num]["wells"][x][0], exp[exp_num]["wells"][y][0]))/(a+b)
		dist_array.at[y, x] = (matchScore(exp[exp_num]["wells"][x][0], exp[exp_num]["wells"][y][0]))/(a+b)
		dist_array.at[x, x] = (matchScore(exp[exp_num]["wells"][x][0], exp[exp_num]["wells"][x][0]))/(a+b)
		dist_array.at[y, y] = (matchScore(exp[exp_num]["wells"][y][0], exp[exp_num]["wells"][y][0]))/(a+b)
		# print(f"Run {exp_num}: "+str(lInter) + f" for {x} ({a}) and {y} ({b}) and they had {lUnion} ins in common")
		#print(str(sumUnion(exp[key]["wells"][x][1], exp[key]["wells"][y][1])) + f"for {x} and {y}")
	print(f"distance array for exp num {exp_num}:")
	print(dist_array)