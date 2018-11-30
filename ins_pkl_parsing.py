import pickle
import pandas as pd

with open("ins_dict.pkl", "rb") as file:
	ins_dict = pickle.load(file)
# nb_dict = {
# 	"pos" : {
# 		"nucleotide" : {
# 			"upstream neighbor" : [count, percent for nuc for pos]
#		}
#	}
#}

nb_dict = {}

for key in ins_dict:
	for i, nuc in enumerate(key):
		if str(i) not in nb_dict:
			nb_dict[str(i)] = {}
		if nuc not in len_dict[str(a)][str(i)]:
			len_dict[str(a)][str(i)][nuc] = [0,0]
		len_dict[str(a)][str(i)][nuc][0] += 1

writer = pd.ExcelWriter('TL_1-8_nuc_vs_pos.xlsx')
for x in len_dict:
	if int(x) <= 20:
		ins_array = pd.DataFrame(columns=["A", "C", "G", "T"], index=[str(i+1) for i in range(int(x))])
		for pos in len_dict[x]:
			nucs_at_pos = 0
			for nuc in len_dict[x][pos]:
				nucs_at_pos += len_dict[x][pos][nuc][0]
			for nuc in len_dict[x][pos]:
				len_dict[x][pos][nuc][1] = round(((len_dict[x][pos][nuc][0] / nucs_at_pos)*100), 3)
				ins_array.at[str(int(pos)+1), nuc] = len_dict[x][pos][nuc][1]
		# file.write(f"Table for length {x} insertions: \n")
		# file.write(ins_array.fillna(0))
		ins_array.fillna(0).to_excel(writer, sheet_name=f"Length {x}")
		writer.save()
