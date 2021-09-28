#include <stdio.h>
#include <stdlib.h>

// Structures
struct Tree {
	int x;
	int y;
	int height;
	int thickness;
	int unit_weight;
	int unit_value;
	int time;
	float rate;
	int status;
};

struct Point {
	int x;
	int y;
} position;

// Variable declarations
int time = 0, time_limit, grid_size, no_trees;
struct Tree *trees;

// Function declarations
void read_input(void);
void greedy_evaluate(struct Tree *tree);
void greedy_evaluate_all(void);
struct Tree *max_value_tree(void);
int is_time_left(int time_required);
void navigate_to(struct Tree *tree);
void cut(struct Tree *tree);
void greedy_navigate(void);
void greedy_approach(void);
int is_tree(int x, int y);
struct Tree *tree_at(int x, int y);
void domino_effect(struct Tree *tree);

// Main loop
int main(int argc, char const *argv[]) {
	read_input();
	greedy_approach();
	return 0;
}

// Function definitions
void read_input(void) {
	scanf(" %d", &time_limit);
	scanf(" %d", &grid_size);
	scanf(" %d", &no_trees);
	trees = (struct Tree *) malloc(sizeof(struct Tree)*no_trees);
	for (int i = 0; i < no_trees; ++i) {
		scanf(" %d", &trees[i].x);
		scanf(" %d", &trees[i].y);
		scanf(" %d", &trees[i].height);
		scanf(" %d", &trees[i].thickness);
		scanf(" %d", &trees[i].unit_weight);
		scanf(" %d", &trees[i].unit_value);
		trees[i].status = 1;
	}
}

void greedy_evaluate(struct Tree *tree) {
	int value = tree->unit_value*tree->height*tree->thickness;
	tree->time = abs(tree->x-position.x)+abs(tree->y-position.y)+tree->thickness;
	tree->rate = ((float)value)/tree->time;
}

void greedy_evaluate_all(void) {
	for (int i = 0; i < no_trees; ++i) {
		if (trees[i].status) {
			greedy_evaluate(&(trees[i]));
		}
	}
}

struct Tree *max_value_tree(void) {
	int max = 0;
	int max_not_set = 1;
	for (int i = 0; i < no_trees; ++i) {
		if (trees[i].status && is_time_left(trees[i].time) && max_not_set) {
			max = i;
			max_not_set = 0;
		}
		else if (trees[i].status && is_time_left(trees[i].time) && !max_not_set && trees[i].rate > trees[max].rate) {
			max = i;
		}
	}
	if (max_not_set) {
		exit(0);
	}
	return &trees[max];
}

int is_time_left(int time_required) {
	if (time+time_required < time_limit) {
		return 1;
	}
	else {
		return 0;
	}
}

void navigate_to(struct Tree *tree) {
	for (int i = 0; i < tree->x-position.x && is_time_left(1); ++i) {
		printf("move right\n");
		time++;
	}
	for (int i = 0; i > tree->x-position.x && is_time_left(1); --i) {
		printf("move left\n");
		time++;
	}
	for (int i = 0; i < tree->y-position.y && is_time_left(1); ++i) {
		printf("move up\n");
		time++;
	}
	for (int i = 0; i > tree->y-position.y && is_time_left(1); --i) {
		printf("move down\n");
		time++;
	}
	position.x = tree->x;
	position.y = tree->y;
}

int is_tree(int x, int y) {
	for (int i = 0; i < no_trees; ++i) {
		if (trees[i].status && x == trees[i].x && y == trees[i].y) {
			return 1;
		}
	}
	return 0;
}

struct Tree *tree_at(int x, int y) {
	for (int i = 0; i < no_trees; ++i) {
		if (x == trees[i].x && y == trees[i].y) {
			return &trees[i];
		}
	}
}

void domino_effect(struct Tree *tree) {
	for (int i = 1; i <= tree->height; ++i) {
		if (is_tree(tree->x, tree->y+i)) {
			struct Tree *tree_under = tree_at(tree->x, tree->y+i);
			int weight_above = tree->unit_weight * tree->height * tree->thickness;
			int weight_below = tree_under->unit_weight * tree_under->height * tree_under->thickness;
			if (weight_above > weight_below) {
				tree_under->status = 0;
				domino_effect(tree_under);
			}
		}
	}
}

void cut(struct Tree *tree) {
	if (is_time_left(tree->thickness)) {
		printf("cut up\n");
		time += tree->thickness;
		tree->status=0;
		domino_effect(tree);
	}
}

void greedy_navigate(void) {
	struct Tree *greedy_tree = max_value_tree();
	navigate_to(greedy_tree);
	cut(greedy_tree);
}

void greedy_approach(void) {
	position.x=0;
	position.y=0;
	while (is_time_left(1)) {
		greedy_evaluate_all();
		greedy_navigate();
	}
}