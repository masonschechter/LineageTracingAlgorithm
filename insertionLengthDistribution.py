import pandas as pd
import pprint
import plotnine as p9
import numpy as np
import matplotlib as plt

distDF = pd.DataFrame(columns=["insLength", "well", "<49", "50+", "total"], index=[])

distDict = {}

for x in range(1,9):
	with open(f"384_well_LT{x}.newinfo.withlengths.sorted.txt") as file:
		for line in file:
			line = line.split('\t')
			ins = line[1]
			insLength = len(line[1])
			insCount = int(line[3])
			well = f"well_{x}"
			if str(insLength) not in distDict:
				distDict[str(insLength)] = {"pool":{"<49":0, "50+":0, "total":0}}
			if well not in distDict[str(insLength)]:
				distDict[str(insLength)][well] = {"<49":0, "50+":0, "total":0}
			if insCount < 50:
				distDict[str(insLength)][well]["<49"] += 1
				distDict[str(insLength)]["pool"]["<49"] += 1
			else:
				distDict[str(insLength)][well]["50+"] += 1
				distDict[str(insLength)]["pool"]["50+"] += 1
			distDict[str(insLength)][well]["total"] += 1
			distDict[str(insLength)]["pool"]["total"] += 1
pp = pprint.PrettyPrinter()
pp.pprint(distDict)

i = 0
for length in distDict:
	if int(length) < 16:
		for sample in distDict[length]:
			distDF.loc[i] = {"insLength":int(length), "well":sample, "<49":distDict[length][sample]["<49"], "50+":distDict[length][sample]["50+"], "total":distDict[length][sample]["total"]}
			i += 1

plot=(p9.ggplot(distDF, p9.aes(x='insLength', y='50+', fill='well'))
    + p9.geom_bar(stat='identity', position='dodge', width=0.9)
    + p9.xlab("Insertion Length")
    + p9.ylab("Count")
    + p9.theme(panel_background=p9.element_rect(fill='white'),
        axis_line_x=p9.element_line(color='black'),
        panel_grid=p9.element_blank(),
        panel_border=p9.element_blank())
    )
plot.__repr__()

