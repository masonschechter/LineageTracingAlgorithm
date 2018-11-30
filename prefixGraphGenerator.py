import prefixTree as pTree

MAX_LENGTH = 3 #YOLOOOOOOO

#Things to keep in mind for consistancy
#	-The children of the tree will be sorted in lexigraphical order at every level
#	-The edge mapping is [parentID]-[childID]

def main():
	tree = pTree.prefixTree()
	q = [] #queue
	inits = ['A','C','G','T']
	for base in inits:
		node = pTree.Node(base,tree.getRoot())
		tree.insert(node)
		q.append(node)

	while q:
		#create the rest of the tree
		node = q.pop(0)
		for base in inits:
			newNode = pTree.Node(node.id+base,node)
			tree.insert(node);
			if not (len(newNode.id) > MAX_LENGTH):
				q.append(newNode)

	print(len(tree.nodes))
	tree.export("prefixData.pkl");

if __name__ == '__main__':
	main()