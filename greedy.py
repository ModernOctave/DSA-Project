import numpy as np
class Tree:
	def __init__(self, x, y, height, thickness, unit_weight, unit_value):
		self.x = x
		self.y = y
		self.height = height
		self.thickness = thickness
		self.unit_weight = unit_weight
		self.unit_value = unit_value
		self.value = height * thickness * unit_value
		self.opt_dir = None
		self.status = True
		self.rate = None

def dominoValue(tree : Tree) :
	# Check domino value in each direction and return max value possible and set direction in tree object.
	pass

def greedyEvaluate(tree : Tree) :
	# Calculate rate and set in tree object
	global pos_x, pos_y
	time = abs(pos_x - tree.x) + abs(pos_y - tree.y) + tree.thickness
	tree.rate = tree.value / time


def greedyEvaluateAll():
	# Calculate rate for all trees which are not cut using greedyEvaluate
	for x in forest:
		if x.status:
			greedyEvaluate(x)

def greedyNavigate():
	# Navigate to tree which is not cut with maximum rate in L-shape
	global pos_x, pos_y
	target = forest[np.argmax([x.rate for x in forest if x.status])]
	while pos_x < target.x:
		print("move right")
		pos_x += 1
	while pos_x > target.x:
		print("move left")
		pos_x -= 1
	while pos_y < target.y:
		print("move up")
		pos_y += 1
	while pos_y > target.y:
		print("move down")
		pos_y -= 1

def greedyCut(tree : Tree):
	# cut tree in optimal direction set status of trees which fall (domino effect too) to false.
	pass

time_limit, grid_size, num_trees = [int(x) for x in input().split(' ')]

forest = []
# 2d array with -1 of grid_size x grid_size
map = np.full((grid_size, grid_size), -1)
for x in range(num_trees):
	data = input().split(' ')
	forest.append(Tree(int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5])))
	map[int(data[0])][int(data[1])] = x

# print(time_limit, grid_size, num_trees)
# print(forest)
# print(map)
