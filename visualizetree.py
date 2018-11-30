import pickle
import prefixTree as pTree
import networkx as nx
import matplotlib.pyplot as plt
import sys

pkl = sys.argv[1]
tree = pTree.prefixTree(pkl)

G = nx.Graph()

for node in tree.nodes:
	if tree.nodes[node].parent:
		G.add_node(tree.nodes[node].id)
		G.add_edge(tree.nodes[node].id, tree.nodes[node].parent.id)
nx.draw(G)