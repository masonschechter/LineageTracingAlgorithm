import pickle
import pandas as pd
import matplotlib.pyplot as plt

with open("ins_dict.pkl", "rb") as file:
	ins_dict = pickle.load(file)
# nb_dict = {
# 	"pos" : {
# 		"nucleotide" : {
# 			"upstream neighbor" : [count, percent for nuc for pos]
#		}
#	}
#}
# final_dict = {
# 	"nucleotide" : {
#		"count" : int
# 		"neighbor" : [count, percent]
# 	}
# }

nb_dict = {}
final_dict = {}

for key in ins_dict:
	for i, nuc in enumerate(key):
		if i == 0:
			continue
		if str(i) not in nb_dict:
			nb_dict[str(i)] = {}
		if nuc not in nb_dict[str(i)]:
			nb_dict[str(i)][nuc] = {}
		if key[i-1] not in nb_dict[str(i)][nuc]:
			nb_dict[str(i)][nuc][key[i-1]] = [0,0]
		nb_dict[str(i)][nuc][key[i-1]][0] += 1


writer = pd.ExcelWriter('TL_1-8_nuc_vs_neighbor.xlsx')
nb_array = pd.DataFrame(columns=["A", "C", "G", "T"], index=["A", "C", "G", "T"])
for x in nb_dict:
	if int(x) <= 20:
		# nb_array = pd.DataFrame(columns=["A", "C", "G", "T"], index=["A", "C", "G", "T"])
		for nuc in nb_dict[x]:
			neighbors_at_pos = 0
			for nb in nb_dict[x][nuc]:
				neighbors_at_pos += nb_dict[x][nuc][nb][0]
			# for nb in nb_dict[x][nuc]:
				# nb_dict[x][nuc][nb][1] = round(((nb_dict[x][nuc][nb][0] / neighbors_at_pos)*100), 3)
				# nb_array.at[nb, nuc] = nb_dict[x][nuc][nb][1]
		# file.write(f"Table for length {x} insertions: \n")
		# file.write(nb_array.fillna(0))
		# nb_array.fillna(0).to_excel(writer, sheet_name=f"Position {str(int(x)+1)}")
		# writer.save()
		# nb_array.fillna(0).plot(kind="bar")
		# plt.show()

for pos in nb_dict:
	if int(pos) <= 20:
		for nuc in nb_dict[pos]:
			neighbors_for_nuc = 0
			if nuc not in final_dict:
				final_dict[nuc] = {"count":0}
			for neigh in nb_dict[pos][nuc]:
				if neigh not in final_dict[nuc]:
					final_dict[nuc][neigh] = [0,0]
				final_dict[nuc]["count"] += nb_dict[pos][nuc][neigh][0]
				final_dict[nuc][neigh][0] += nb_dict[pos][nuc][neigh][0]

for nuc in final_dict:
	for nb in final_dict[nuc]:
		if not nb == "count":
			final_dict[nuc][nb][1] = round(((final_dict[nuc][nb][0] / final_dict[nuc]["count"])*100), 3)
			nb_array.at[nuc,nb] = final_dict[nuc][nb][1]
print(final_dict)
print(nb_array)
barchart = nb_array.fillna(0).plot(kind='box')
barchart.set_xlabel('appended nucleotide')
barchart.set_ylabel('percent chance of appended nucleotide with given neighbor')
plt.show()