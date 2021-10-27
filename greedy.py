import numpy as np
from enum import Enum
class Tree:
	def __init__(self, x, y, height, thickness, unit_weight, unit_value):
		self.x = x
		self.y = y
		self.height = height
		self.thickness = thickness
		self.unit_weight = unit_weight
		self.unit_value = unit_value
		self.value = height * thickness * unit_value
		self.weight = height * thickness * unit_weight
		self.opt_dir = None
		self.status = True
		self.rate = None

class Direction(Enum):
	RIGHT = 0
	LEFT = 1
	UP = 2
	DOWN = 3

def isTree(x_postion,y_postion):
	if map[x_postion, y_postion] != -1 and forest[map[x_postion,y_postion]].status :
		return True
	return False

def dominoValueInDir(tree : Tree, dir):
	if dir == Direction.RIGHT:
		val = 0
		for x in range(tree.height):
			if tree.x + x < grid_size :
				if  isTree(tree.x + x,tree.y): 
					falling_tree = forest[map[tree.x+x,tree.y]]
					if tree.weight > falling_tree.weight:
						val += falling_tree.value + dominoValueInDir(falling_tree, dir)
					else:
						break
			else:
				break

	if dir == Direction.LEFT:
		val = 0
		for x in range(tree.height):
			if tree.x - x >= 0 :
				if isTree(tree.x - x, tree.y):  
					falling_tree = forest[map[tree.x-x,tree.y]]
					if tree.weight > falling_tree.weight:
						val += falling_tree.value + dominoValueInDir(falling_tree, dir)
					else:
						break
			else:
				break

	if dir == Direction.UP:
		val = 0
		for x in range(tree.height):
			if tree.y + x < grid_size:
				if isTree(tree.x, tree.y + x): 
					falling_tree = forest[map[tree.x,tree.y+x]]
					if tree.weight > falling_tree.weight:
						val += falling_tree.value + dominoValueInDir(falling_tree, dir)
					else:
						break
			else:
				break

	if dir == Direction.DOWN:
		val = 0
		for x in range(tree.height):
			if tree.y - x >= 0 :
				if isTree(tree.x,tree.y - x):  
					falling_tree = forest[map[tree.x,tree.y-x]]
					if tree.weight > falling_tree.weight:
						val += falling_tree.value + dominoValueInDir(falling_tree, dir)
					else:
						break
			else:
				break

	return val

def dominoValue(tree : Tree) :
	# Check domino value in each direction and return max value possible and set direction in tree object.

	dir_right = dominoValueInDir(tree, Direction.RIGHT)
	dir_left = dominoValueInDir(tree, Direction.LEFT)
	dir_up = dominoValueInDir(tree, Direction.UP)
	dir_down = dominoValueInDir(tree, Direction.DOWN)

	opt_value = max(val_right, val_left, val_up, val_down)
	if opt_value == val_right :
		tree.opt_dir = Direction.RIGHT
	elif opt_value == val_left:
		tree.opt_dir = Direction.LEFT
	elif opt_value == val_up:
		tree.opt_dir = Direction.UP
	else :
		tree.opt_dir = Direction.DOWN
	
	return opt_value

def greedyEvaluate(tree : Tree) :
	# Calculate rate and set in tree object
	time = abs(pos_x - tree.x) + abs(pos_y - tree.y) + tree.thickness
	tree.rate = tree.value / time

def greedyEvaluateAll():
	# Calculate rate for all trees which are not cut using greedyEvaluate
	for x in forest:
		if x.status:
			greedyEvaluate(x)

def greedyNavigate():
	# Navigate to tree which is not cut with maximum rate in L-shape
	pass

def greedyCut(tree : Tree):
	# cut tree in optimal direction set status of trees which fall (domino effect too) to false.
	pass

def isTimeLeft(x):
	if time_limit-time >= x:
		return True
	else
		return False

time_limit, grid_size, num_trees = [int(x) for x in input().split(' ')]
pos_x = 0
pos_y = 0
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