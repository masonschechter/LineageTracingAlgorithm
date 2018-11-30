import pickle
import sys

ins_dict = {}

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

with open(sys.argv[1]) as samples:
	for line in samples:
		counter = 0
		c = 0
		count = 0
		ins_count = 0
		seq_count = 0
		line = line.strip().split(' ')
		seq_file = line[0]
		newinfo = line[1]
		withlengths = line[2]
		well = line[3]
		print(f"Working on {well}")

		with open(withlengths) as lengths:
			for line in lengths:
				ins_info = line.strip().split('\t')
				insertion = ins_info[1]
				ins_len = ins_info[2]
				ins_count = int(ins_info[3])
				ins_perc = ins_info[4]
				if insertion not in ins_dict.keys():
					ins_dict[insertion] = {"seqs":{well:[]}, "umis":{well:[]}, "counts":{well:ins_count}}
					c += 1
				else:
					if well in ins_dict[insertion]["counts"]:
						ins_dict[insertion]["counts"][well] += ins_count
					else:
						ins_dict[insertion]["seqs"][well] = []
						ins_dict[insertion]["umis"][well] = []
						ins_dict[insertion]["counts"][well] = ins_count
						ins_count += 1
			print(f"{c} unique insertions in {well}")
			print(f"{ins_count} non-unique in {well}")

		with open(newinfo) as info:
			for line in info:
				seq_info = line.strip().split('\t')
				if not seq_info[3] == 'ROOT':
					seq = seq_info[0]
					insertion = seq_info[3]
					if insertion in ins_dict.keys():
						if well in ins_dict[insertion]["seqs"]:
							ins_dict[insertion]["seqs"][well].append(seq)
						else:
							ins_dict[insertion]["seqs"][well] = []
							ins_dict[insertion]["seqs"][well].append(seq)
					else:
						# print(insertion, well)
						counter += 1
			print(f"{counter} left behind for {well}")

		with open(seq_file) as seqs:
			for line in seqs:
				seq_count += 1
				umi_info = line.strip().split('\t')
				umi = umi_info[0]
				seq = umi_info[1]
				for key in ins_dict:
					if seq in ins_dict[key]["seqs"]:
						if well in ins_dict[key]["umis"]:
							ins_dict[key]["umis"][well].append(umi)
						else:
							ins_dict[key]["umis"][well] = []
							ins_dict[key]["umis"][well].append(umi)					
			print(f"{seq_count} total seqs in {well}")

for key in ins_dict:
	unique = 0
	for well in ins_dict[key]["umis"]:
		unique += len(ins_dict[key]["umis"][well])
		print(f"{unique} unique occurences of {key} in {well}")

with open('ins_dict.pkl', 'wb') as file:
	pickle.dump(ins_dict, file)





