import pickle






with open('TL18_umi_pickle.pkl', 'rb') as file:
	umi_dict = pickle.load(file)

with open('TL18_umi_info.txt', 'w') as outfile:
	outfile.write('umi' + '\t' + 'well' + '\t' + 'insertion' + '\n')
	for key in umi_dict:
		outfile.write(key + '\t' + umi_dict[key]["well"] + '\t' + umi_dict[key]["ins"] + '\n')	