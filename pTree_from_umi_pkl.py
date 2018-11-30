import pickle
import prefixTree as pTree
from graphviz import Digraph, Source, nohtml, Graph

g = Graph('g', filename='insTree.gv',node_attr={'shape': 'record', 'height': '.1','width':'1.0'},graph_attr={'ranksep':".5"})
tree = pTree.PrefixTree() #empty tree
with open('TL_1-8_umi_pickle.pkl', 'rb') as file:
	umi_dict = pickle.load(file)

# for key in umi_dict:
# 	print(key)

counter = 0
q = []
for key in umi_dict:
	if counter >= 10000:
		break;
	if len(umi_dict[key]["ins"]) < 15:
		if umi_dict[key]["ins_count"] > 3:
			q.append(umi_dict[key]["ins"])
	counter +=1
q.sort();
for key in q:
	print("Inserting: "+key)
	node = pTree.Node(key,None)
	tree.insert(node,tree.getRoot())
	counter+=1

for node in tree.nodes:
	if tree.nodes[node].parent:
		if tree.nodes[node].isGhost():
			g.node(tree.nodes[node].id,_attributes={"shape":"point"})
		else:
			g.node(tree.nodes[node].id)
		g.edge(tree.nodes[node].parent.id,tree.nodes[node].id,)#_attributes={'penwidth':str(tree.edges[tree.nodes[node].parent.id+"-"+tree.nodes[node].id]/2)})
	else:
		g.node(tree.nodes[node].id,_attributes={"shape":"point"})
g.view()