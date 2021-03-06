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
		self.time = None
		self.affects_up = 0
		self.affects_down = 0
		self.affects_left = 0
		self.affects_right = 0
		
class Direction(Enum):
	RIGHT = 0
	LEFT = 1
	UP = 2
	DOWN = 3

def isTree(x_postion,y_postion):
	if x_postion < grid_size and x_postion >=0:
		if y_postion < grid_size and y_postion >=0:
			if map[x_postion, y_postion] != -1 and forest[map[x_postion,y_postion]].status :
				return True
	return False

def returnAffects(tree :Tree, dir):
	if dir == Direction.RIGHT:
		if tree.affects_right == 0:
			# Calculate right
			for i in range(1, tree.height):
				if tree.x + i < grid_size :
					if  isTree(tree.x + i,tree.y):
						falling_tree = forest[map[tree.x+i,tree.y]]
						if tree.weight > falling_tree.weight:
							tree.affects_right += falling_tree.value
							tree.affects_right += returnAffects(falling_tree, dir)
							break
						else:
							break
				else:
					break
		return tree.affects_right

	if dir == Direction.LEFT:
		if tree.affects_left == 0:
			# Calculate for left
			for i in range(1, tree.height):
				if tree.x - i >= 0 :
					if isTree(tree.x - i, tree.y):  
						falling_tree = forest[map[tree.x-i,tree.y]]
						if tree.weight > falling_tree.weight:
							tree.affects_left += falling_tree.value
							tree.affects_left += returnAffects(falling_tree, dir)
							break
						else:
							break
				else:
					break
		return tree.affects_left

	if dir == Direction.UP:
		if tree.affects_up == 0:
			# Calculate for up
			for i in range(1, tree.height):
				if tree.y + i < grid_size :
					if isTree(tree.x, tree.y + i):
						falling_tree = forest[map[tree.x,tree.y+i]]
						if tree.weight > falling_tree.weight:
							tree.affects_up += falling_tree.value
							tree.affects_up += returnAffects(falling_tree, dir)
							break
						else:
							break
				else:
					break
		return tree.affects_up
		
	if dir == Direction.DOWN:
		if tree.affects_down == 0:
			# Calculate for down
			for i in range(1, tree.height):
				if tree.y - i >= 0 :
					if isTree(tree.x, tree.y - i):
						falling_tree = forest[map[tree.x,tree.y-i]]
						if tree.weight > falling_tree.weight:
							tree.affects_down += falling_tree.value
							tree.affects_down += returnAffects(falling_tree, dir)
							break
						else:
							break	
				else:
					break			
		return tree.affects_down

def dominoValueInDir( tree : Tree, dir):
	val = 0
	dominoTrees = [x for x in returnAffects(tree, dir) if x.status]
	for falling_tree in dominoTrees:
		val += falling_tree.value
	return val
			
	# if dir == Direction.RIGHT:
		
	# if dir == Direction.LEFT:
	# 	val = 0
	# 	dominoTrees = [x for x in tree.affects_left if forest.status]
	# 	for falling_tree in dominoTrees:
	# 		val += falling_tree.value
	# 		if tree.x - tree.height > falling_tree.x - falling_tree.height:
	# 			val += dominoValueInDir(falling_tree, dir)

	# if dir == Direction.UP:
	# 	val = 0
	# 	dominoTrees = [x for x in tree.affects_up if forest.status]
		
	# if dir == Direction.DOWN:
	# 	val = 0
	# 	dominoTrees = [x for x in tree.affects_down if forest.status]

	# add the value of each tree in dominoTrees to val


def dominoValue(tree : Tree) :
	# Check domino value in each direction and return max value possible and set direction in tree object.

	val_right = returnAffects(tree, Direction.RIGHT)
	val_left = returnAffects(tree, Direction.LEFT)
	val_up = returnAffects(tree, Direction.UP)
	val_down = returnAffects(tree, Direction.DOWN)
	opt_value = max(val_right, val_left, val_up, val_down)
	if opt_value == val_right:
		tree.opt_dir = Direction.RIGHT
	elif opt_value == val_left:
		tree.opt_dir = Direction.LEFT
	elif opt_value == val_up:
		tree.opt_dir = Direction.UP
	else :
		tree.opt_dir = Direction.DOWN
	# print(tree.x, tree.y, val_right, val_left, val_up, val_down)
	return opt_value

def greedyEvaluate(tree : Tree) :
	# Calculate rate and set in tree object
	global pos_x, pos_y
	tree.time = abs(pos_x - tree.x) + abs(pos_y - tree.y) + tree.thickness
	tree.rate = (tree.value + dominoValue(tree)) / tree.time

def greedyEvaluateAll():
	# Calculate rate for all trees which are not cut using greedyEvaluate
	for x in forest:
		if x.status:
			greedyEvaluate(x)
	# print([x.status for x in forest])

def greedyNavigate():
	# Navigate to tree which is not cut with maximum rate in L-shape
	global pos_x, pos_y, time_elapsed, is_time_left
	target = None
	for y in np.argsort([-1*x.rate for x in forest]):	# To see.
		if forest[y].status and isTimeLeft(forest[y].time):
			target = forest[y]
			break
	if target == None:
		is_time_left = False
		return
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

def greedyCut():
	# cut tree in optimal direction set status of trees which fall (domino effect too) to false.
	global pos_x, pos_y, time_elapsed, is_time_left
	tree = forest[map[pos_x][pos_y]]
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
	tree.status = False
	tree.rate = 0
	dominoEffect(tree, tree.opt_dir)

def dominoEffect(tree : Tree, dir):
	# dominoTrees = [x for x in returnAffects(tree, dir) if x.status]
	# for falling_tree in dominoTrees:
	# 	falling_tree.status = False
	# 	falling_tree.rate = 0

	# dominoTrees = []

	if dir == Direction.UP:
		for i in range(1, tree.height):
			if tree.y+i < grid_size:
				if isTree(tree.x, tree.y+i):
					falling_tree = forest[map[tree.x][tree.y+i]]
					if tree.weight > falling_tree.weight:
						falling_tree.status = False
						falling_tree.rate = 0
						if tree.y + tree.height < falling_tree.y + falling_tree.height:
							# dominoTrees.append(falling_tree)
							dominoEffect(falling_tree, dir)
					else:
						break
			else:
				break

	elif dir == Direction.DOWN:
		for i in range(1, tree.height):
			if tree.y-i >= 0:
				if isTree(tree.x, tree.y-i):
					falling_tree = forest[map[tree.x][tree.y-i]]
					if tree.weight > falling_tree.weight:
						falling_tree.status = False
						falling_tree.rate = 0
						if tree.y - tree.height > falling_tree.y - falling_tree.height:
							# dominoTrees.append(falling_tree)
							dominoEffect(falling_tree, dir)
					else:
						break
			else:
				break

	elif dir == Direction.RIGHT:
		for i in range(1, tree.height):
			if tree.x + i < grid_size:
				if isTree(tree.x+i, tree.y):
					falling_tree = forest[map[tree.x+i][tree.y]]
					if tree.weight > falling_tree.weight:
						falling_tree.status = False
						falling_tree.rate = 0
						if tree.x + tree.height < falling_tree.x + falling_tree.height:
							# dominoTrees.append(falling_tree)
							dominoEffect(falling_tree, dir)
					else:
						break
			else:
				break

	elif dir == Direction.LEFT:
		for i in range(1, tree.height):
			if tree.x - i >= 0:
				if isTree(tree.x-i, tree.y):
					falling_tree = forest[map[tree.x-i][tree.y]]
					if tree.weight > falling_tree.weight:
						falling_tree.status = False
						falling_tree.rate = 0
						if tree.x - tree.height > falling_tree.x - falling_tree.height:
							# dominoTrees.append(falling_tree)
							dominoEffect(falling_tree, dir)
					else:
						break
			else:
				break

	# for x in dominoTrees:
	# 	dominoEffect(x, dir)

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
	if is_time_left:
		if isTree(pos_x, pos_y):
			greedyCut()
		# empty all affects_dir lists of forests to none
		for tree in forest:
			tree.affects_up = 0
			tree.affects_down = 0
			tree.affects_left = 0
			tree.affects_right = 0