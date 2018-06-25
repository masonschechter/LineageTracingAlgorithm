import pickle
import gzip

class Node():
	def __init__(self, name, parent):
		self.id = name
		self.parent = parent

	def __str__(self):
		return self.id


class prefixTree():
	def __init__(self,treeFile=None,):
		if treeFile:
			self.loadFromFile(treeFile)
		else:
			# Create root node and add to dicts
			self.root = Node("0",None)
			self.edges = {"0":0}
			self.nodes = {"0":self.root}

	def getRoot(self):
		return self.root

	def insert(self,node):
		# insert node into node dict, and link to parent
		self.nodes[node.id] = node
		self.edges[node.parent.id+"-"+node.id] = 0

	def getNode(self, name):
		return self.nodes[name]

	def updateWeights(self,node):
		if node.parent == None:
			return
		self.edges[self.getEdge(node)] += 1
		self.updateWeights(node.parent)

	def getEdge(self,node):
		return node.parent.id+"-"+node.id

	def export(self,treeFile):
		with open(treeFile, 'wb') as file:
			data = {"nodes":self.nodes,"edges":self.edges}
			pickle.dump(data, file)

	def loadFromFile(self,treeFile):
		with open(treeFile, 'rb') as file:
			data = pickle.load(file)
			self.nodes = data["nodes"]
			self.edges = data["edges"]