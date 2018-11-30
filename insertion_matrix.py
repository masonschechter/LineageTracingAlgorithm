import pickle
import pandas as pd
from itertools import combinations
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt


with open('384_well_LT_ins_dict.pkl', 'rb') as file:
	ins_dict = pickle.load(file)

# well_dict = {
# 	"well": {
# 		"ins": {
# 			"umi_count": int()
# 			"ins_count": int()
# 		}
# 	}
# }
def matchScore(ins1,ins2):
	match = 0
	if len(ins1) > len(ins2):
		for i, nuc in enumerate(ins2):
			if ins1[i] == nuc:
				match += 1
			else:
				break
	else:
		for i, nuc in enumerate(ins1):
			if ins2[i] == nuc:
				match += 1
			else:
				break
	score = (match/len(ins1) + match/len(ins2))/2
	return score

well_dict = {}
for ins in ins_dict:
	if not ins == 'ROOT':
		if len(ins) in range(7,15):
			for well in ins_dict[ins]["counts"]:
				if ins_dict[ins]["counts"][well] >= 50:
					if well not in well_dict:
						well_dict[well] = {}
						well_dict[well][ins] = {"ins_count":0}
					else:
						well_dict[well][ins] = {"ins_count":0}
					well_dict[well][ins]["ins_count"] = ins_dict[ins]["counts"][well]

wells = ['well_1', 'well_2', 'well_3', 'well_4', 'well_5', 'well_6', 'well_7', 'well_8']

distDF = pd.DataFrame(columns=[x for x in wells], index=[x for x in wells])

for x,y in combinations(wells, 2):
	lenX = len(well_dict[x])
	lenY = len(well_dict[y])
	insDF = pd.DataFrame(columns=[i for i in well_dict[x]], index=[n for n in well_dict[y]])
	for r in insDF.index:
		for c in insDF.columns:
			insDF.loc[r,c] = matchScore(r,c)
	xWeight = 0
	yWeight = 0
	for c in insDF.columns:
		xWeight += insDF[c].max()
	for r in insDF.index:
		yWeight += insDF.loc[r].max()
	distDF.loc[x,y] = ((xWeight/lenX) + (yWeight/lenY))/2
	distDF.loc[y,x] = ((xWeight/lenX) + (yWeight/lenY))/2
	distDF.loc[x,x] = 1
	distDF.loc[y,y] = 1
print(insDF)

# z = hierarchy.linkage(distDF, 'average')#, optimal_ordering=True)
# plt.figure()

# dn = hierarchy.dendrogram(z)
# plt.show()


