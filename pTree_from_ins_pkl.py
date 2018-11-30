import pickle
import prefixTree as pTree
# from graphviz import Digraph, Source, nohtml, Graph
from operator import itemgetter

# g = Graph('g', filename='insTree.gv',node_attr={'shape': 'record', 'height': '.1','width':'1.0'},graph_attr={'ranksep':".5"})
# tree = pTree.PrefixTree() #empty tree
with open('Nov2018_384LT_insDict.pkl', 'rb') as file:
	insDict = pickle.load(file)

# insDict = {
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

# wellDict = {
# 	"well": {
# 		"ins": {
# 			"umi_count": int()
# 			"insCount": int()
# 		}
# 	}
# }
wellDict = {}
for ins in insDict:
	if not ins == 'ROOT':
		if len(ins) in range(8,15):
			for well in insDict[ins]["counts"]:
				if insDict[ins]["counts"][well] >= 10:
					if well not in wellDict:
						wellDict[well] = {}
						wellDict[well][ins] = {"insCount":0}
					else:
						wellDict[well][ins] = {"insCount":0}
					wellDict[well][ins]["insCount"] = insDict[ins]["counts"][well]

with open('wellDict.pkl', 'wb') as file:
	pickle.dump(wellDict, file)

for well in wellDict:
	print(f"{len(wellDict[well])} insertions for {well}, 0-16")
	q = []
	# g = Graph('g', filename=f'{well}_insTree.gv',node_attr={'shape': 'record', 'height': '.1','width':'1.0'},graph_attr={'ranksep':".5"})
	tree = pTree.PrefixTree()
	for ins in wellDict[well]:
		q.append(ins)
	q = sorted(q, key=itemgetter(0))
	for ins in q:
		# print(f"Inserting {ins}")
		node = pTree.Node(ins,None)
		tree.insert(node,tree.getRoot())
		# print(tree.nodes[node.id].parent)
	# for node in tree.nodes:
	# 	if tree.nodes[node].parent:
	# 		if tree.nodes[node].isGhost():
	# 			g.node(tree.nodes[node].id,_attributes={"shape":"point"})
	# 		else:
	# 			g.node(tree.nodes[node].id)
	# 		g.edge(tree.nodes[node].parent.id,tree.nodes[node].id,)#_attributes={'penwidth':str(tree.edges[tree.nodes[node].parent.id+"-"+tree.nodes[node].id]/2)})
	# 	else:
	# 		g.node(tree.nodes[node].id,_attributes={"shape":"point"})
	tree.export(f"{well}_insTree.pkl")
# counter = 0
# q = []
# for key in insDict:
# 	if counter >= 10000:
# 		break;
# 	if len(insDict[key]["ins"]) < 15:
# 		if insDict[key]["insCount"] > 3:
# 			q.append(insDict[key]["ins"])
# 	counter +=1
# q.sort();
# for key in q:
# 	print("Inserting: "+key)
# 	node = pTree.Node(key,None)
# 	tree.insert(node,tree.getRoot())
# 	counter+=1

wells = [x for x in wellDict]
pool = []
pooledTree = pTree.PrefixTree()
for well in wells:
	wellTree = pTree.PrefixTree(treeFile=f"{well}_insTree.pkl")
	wellNodes = [x for x in wellTree.nodes]
	for n in wellNodes:
		if n not in pool:
			pool.append(n)
for n in pool:
	node = pTree.Node(n,None)
	pooledTree.insert(node, pooledTree.getRoot())
pooledTree.export('pooled_insTree.pkl')
