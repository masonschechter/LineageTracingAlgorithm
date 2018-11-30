import sys
import pickle


#{umi: {"seq": str,
#		"well": str, 
#		"ins": str, 
#		"ins_len": int, 
#		"ins_count": int, 
#		"ins_percent": float 
#		}}

#results/temp_for_umi/well.seq
#umi /t sequence

#results/insertions/well.newinfo.txt
#sequence /t MIDX /t cut position /t insertion or ROOT

#results/insertions/well.newinfo.withlengths.sorted.txt
#cut position /t insertion /t len of insertion /t number of reads with insertion /t percentage of reads with insertion
umi_dict = {}

with open(sys.argv[1], 'r') as samples:
	for line in samples:
		line = line.strip().split(' ')
		seq_file = line[0]
		newinfo = line[1]
		withlengths = line[2]
		well = line[3]
		print(f"Working on {well}")
		with open(seq_file, 'r') as seqs:
			for line in seqs:
				umi_info = line.strip().split('\t')
				umi_dict[umi_info[0]] = {"seq":umi_info[1]}
				umi_dict[umi_info[0]]["well"] = well


		with open(newinfo, 'r') as info:
			for line in info:
				seq_info = line.strip().split('\t')
				if not seq_info[3] == 'ROOT':
					seq = seq_info[0]
					insertion = seq_info[3]
					for key in umi_dict:
						if seq == umi_dict[key]["seq"] and "ins" not in umi_dict[key]:
							umi_dict[key]["ins"] = insertion
							break

		del_q = []
		for key in umi_dict:
			if "ins" not in umi_dict[key]:
				del_q.append(key)

		for key in del_q:
			del umi_dict[key]

		with open(withlengths, 'r') as lens:
			for line in lens:
				ins_info = line.strip().split('\t')
				insertion = ins_info[1]
				ins_len = ins_info[2]
				ins_count = ins_info[3]
				ins_perc = ins_info[4]
				for key in umi_dict:
					if insertion == umi_dict[key]["ins"]:
						umi_dict[key]["ins_len"] = int(ins_len)
						umi_dict[key]["ins_count"] = int(ins_count)
						umi_dict[key]["ins_percent"] = float(ins_perc)

outfile = 'TL_1-8_umi_pickle.pkl'
with open(outfile, 'wb') as file:
	pickle.dump(umi_dict, file)






