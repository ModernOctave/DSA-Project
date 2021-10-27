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
		self.domino_trees = []
		self.status = True
		self.rate = None
		self.time = None

class Direction(Enum):
	RIGHT = 0
	LEFT = 1
	UP = 2
	DOWN = 3

def isTree(x_postion,y_postion):
	if map[x_postion, y_postion] != -1 and forest[map[x_postion,y_postion]].status :
		return True
	return False

def dominoValueInDir(first_tree : Tree, tree : Tree, dir):
	if first_tree == tree:
		first_tree.domino_trees = []

	if dir == Direction.RIGHT:
		val = 0
		for x in range(tree.height):
			if tree.x + x < grid_size :
				if  isTree(tree.x + x,tree.y): 
					falling_tree = forest[map[tree.x+x,tree.y]]
					if tree.weight > falling_tree.weight:
						val += falling_tree.value + dominoValueInDir(first_tree, falling_tree, dir)
						first_tree.domino_trees.append(falling_tree)
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
						val += falling_tree.value + dominoValueInDir(first_tree, falling_tree, dir)
						first_tree.domino_trees.append(falling_tree)
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
						val += falling_tree.value + dominoValueInDir(first_tree, falling_tree, dir)
						first_tree.domino_trees.append(falling_tree)
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
						val += falling_tree.value + dominoValueInDir(first_tree, falling_tree, dir)
						first_tree.domino_trees.append(falling_tree)
					else:
						break
			else:
				break

	return val

def dominoValue(tree : Tree) :
	# Check domino value in each direction and return max value possible and set direction in tree object.

	val_right = dominoValueInDir(tree, tree, Direction.RIGHT)
	val_left = dominoValueInDir(tree, tree, Direction.LEFT)
	val_up = dominoValueInDir(tree, tree, Direction.UP)
	val_down = dominoValueInDir(tree, tree, Direction.DOWN)

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
	global pos_x, pos_y
	tree.time = abs(pos_x - tree.x) + abs(pos_y - tree.y) + tree.thickness
	tree.rate = tree.value + dominoValue(tree) / tree.time

def greedyEvaluateAll():
	# Calculate rate for all trees which are not cut using greedyEvaluate
	for x in forest:
		if x.status:
			greedyEvaluate(x)

def greedyNavigate():
	# Navigate to tree which is not cut with maximum rate in L-shape
	global pos_x, pos_y, time_elapsed, is_time_left
	target = None;
	for y in np.argsort([x.rate for x in forest if x.status]):
		if isTimeLeft(forest[y].time):
			target = forest[y]
			print(target.x, target.y, target.time)
			break
	if target == None:
		is_time_left = False
		return
	if isTimeLeft(target.time):
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
		time_elapsed += target.time
	else:
		is_time_left = False

def greedyCut():
	# cut tree in optimal direction set status of trees which fall (domino effect too) to false.
	global pos_x, pos_y, time_elapsed, is_time_left
	tree = forest[map[pos_x][pos_y]]
	if isTimeLeft(tree.thickness):
		if tree.opt_dir == Direction.UP:
			print('cut up')
			time_elapsed += tree.thickness
		elif tree.opt_dir == Direction.DOWN:
			print('cut down')
			time_elapsed += tree.thickness
		elif tree.opt_dir == Direction.RIGHT:
			print('cut right')
			time_elapsed += tree.thickness
		elif tree.opt_dir == Direction.LEFT:
			print('cut left')
			time_elapsed += tree.thickness
		print(tree.status)
		tree.status = False
		print(tree.status)
		for x in tree.domino_trees:
			x.status = False
	else:
		is_time_left = False

def isTimeLeft(x):
	global time_elapsed, is_time_left
	if time_limit >= time_elapsed + x:
		return True
	else:
		return False

# Initialized variables
pos_x = 0
pos_y = 0
forest = []
is_time_left = True
time_elapsed = 0

# Read inputs
time_limit, grid_size, num_trees = [int(x) for x in input().split(' ')]

# Initialize grid
map = np.full((grid_size, grid_size), -1)

for x in range(num_trees):
	data = input().split(' ')
	forest.append(Tree(int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5])))
	map[int(data[0])][int(data[1])] = x

# Main algorithm
while is_time_left:
	greedyEvaluateAll()
	greedyNavigate()
	greedyCut()
