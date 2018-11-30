import pickle
import sys
import pprint

insDict = {}

# insDict = {
	# insertion:{		
# 		"counts": {
#			"well" : int()
#		}
# 	}
# }

with open(sys.argv[1]) as samples:
	for line in samples:
		counter = 0
		c = 0
		count = 0
		insCount = 0
		line = line.strip().split(' ')
		withlengths = line[0]
		well = "well_" + line[0][6:7]
		print(f"Working on {well}")

		with open(withlengths) as lengths:
			for line in lengths:
				insInfo = line.strip().split('\t')
				insertion = insInfo[1]
				insLen = insInfo[2]
				insCount = int(insInfo[3])
				insPerc = insInfo[4]
				if insertion == 'ROOT':
					print("found one")
					continue
				if insertion not in insDict:
					insDict[insertion] = {"counts":{well:insCount}}
					c += 1
					continue
				if well in insDict[insertion]["counts"]:
					insDict[insertion]["counts"][well] += insCount
				else:
					insDict[insertion]["counts"][well] = insCount
			# print(f"{c} unique insertions in {well}")
			# print(f"{insCount} non-unique in {well}")

countDict = {}

for key in insDict:
	for w in insDict[key]["counts"]:
		if not w in countDict:
			countDict[w] = 1
		else:
			countDict[w] += 1


pp = pprint.PrettyPrinter(indent=4)
pp.pprint(countDict)

with open('Nov2018_384LT_insDict.pkl', 'wb') as file:
	pickle.dump(insDict, file)
