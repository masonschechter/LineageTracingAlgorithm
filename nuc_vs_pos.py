import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
# } ### A pickled ins_dict would be the best output.
### the rest of the scripts parse the ins_dict in different ways.
### this guy will generate a plot of nucleotide identiy vs position.
### based in seaborn (matplotlib on crack) so I could easily generate a heat map
### but the data looked better in bar graph/histogram form tbh

with open("ins_dict.pkl", "rb") as file:
	ins_dict = pickle.load(file)
# len_dict = {
# 	"length" : {
# 		"position" : {
# 			"nucleotide" : [count, percent @ position]
#		}
#	}
#}

final_dict = {}

len_dict = {}

for key in ins_dict:
	a = len(key)
	if a <= 20:
		if str(a) not in len_dict:
			len_dict[str(a)] = {}
		for i, nuc in enumerate(key):
			if str(i) not in len_dict[str(a)]:
				len_dict[str(a)][str(i)] = {}
			if str(i) not in final_dict:
				final_dict[str(i)] = {"count":0, "nucs":{}}
			if nuc not in len_dict[str(a)][str(i)]:
				len_dict[str(a)][str(i)][nuc] = [0,0]
			if nuc not in final_dict[str(i)]["nucs"]:
				final_dict[str(i)]["nucs"][nuc] = [0,0]
			len_dict[str(a)][str(i)][nuc][0] += 1

ins_array = pd.DataFrame(columns=["A", "C", "G", "T"], index=[str(i+1) for i in range(int(20))])
# writer = pd.ExcelWriter('TL_1-8_nuc_vs_pos.xlsx')
for x in len_dict:
	if int(x) <= 20:
		# ins_array = pd.DataFrame(columns=["A", "C", "G", "T"], index=[str(i+1) for i in range(int(x))])
		for pos in len_dict[x]:
			nucs_at_pos = 0
			for nuc in len_dict[x][pos]:
				nucs_at_pos += len_dict[x][pos][nuc][0]
				final_dict[pos]["count"] += len_dict[x][pos][nuc][0]
				final_dict[pos]["nucs"][nuc][0] += len_dict[x][pos][nuc][0]
			for nuc in len_dict[x][pos]:
				len_dict[x][pos][nuc][1] = round(((len_dict[x][pos][nuc][0] / nucs_at_pos)*100), 3)
		# file.write(f"Table for length {x} insertions: \n")
		# file.write(ins_array.fillna(0))
		# ins_array.fillna(0).to_excel(writer, sheet_name=f"Length {x}")
		# writer.save()

for pos in final_dict:
	for nuc in final_dict[pos]["nucs"]:
		final_dict[pos]["nucs"][nuc][1] = round(((final_dict[pos]["nucs"][nuc][0]/final_dict[pos]["count"])*100), 3)
		ins_array.at[str(int(pos)+1), nuc] = final_dict[pos]["nucs"][nuc][1]

# print(ins_array.fillna(0))
# barchart = ins_array.fillna(0).plot(kind='bar')
# barchart.set_xlabel('position in insertion')
# barchart.set_ylabel('percent of nucleotides appended at position')
# plt.show()

hm = sns.heatmap(ins_array.fillna(0), square=True, cmap="Spectral_r")
plt.show()