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


def dominoValue(tree : Tree) :
	# Check domino value in each direction and return max value possible and set direction in tree object.

	val_right = 0
	for x in range(tree.height):
		if tree.x + x < grid_size :
			if  isTree(tree.x + x,tree.y): 
				if tree.weight > forest[map[tree.x,tree.y+x]].weight:
					val_right += forest[map[tree.x,tree.y+x]].value
				else:
					break
		else:
			break

	val_left = 0
	for x in range(tree.height):
		if tree.x - x >= 0 :
			if isTree(tree.x - x, tree.y): 
				if tree.weight > forest[map[tree.x,tree.y + x]].weight:
					val_left += forest[map[tree.x,tree.y + x]].value
				else:
					break
		else:
			break
	
	val_up = 0
	for x in range(tree.height):
		if tree.y + x < grid_size:
			if isTree(tree.x, tree.y + x):
				if tree.weight > forest[map[tree.x, tree.y + x]].weight:
					val_up += forest[map[tree.x, tree.y + x]].value
				else:
					break
		else:
			break

	val_down = 0
	for x in range(tree.height):
		if tree.y - x >= 0 :
			if isTree(tree.x,tree.y - x): 
				if tree.weight > forest[map[tree.x, tree.y + x]].weight:
					val_down += forest[map[tree.x, tree.y + x]].value
				else:
					break
		else:
			break


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
