/*
						 DSA Lab Project
	Lumberjack Problem [https://www.optil.io/optilion/problem/3000]

				  Algorithmic Crushers (Group 14)

				 Chirumamilla Bharghav (200010010)
				   Josyula Abhishek (200010021)
				      M V Karthik (200010030)
				       Om Patil (200010036)
*/

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
	int value;
	int weight;
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
void domino_effect(int side, struct Tree *tree);
int domino_value(int side, struct Tree *tree);

// Linked List Function Declarations
struct node *insert_beginning(struct node *head, struct Tree *data);
struct Tree *value_at(struct node *head, int pos);
struct node *delete_from(struct node *head, int pos);

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
		trees[i].value = trees[i].unit_value * trees[i].height * trees[i].thickness;
		trees[i].weight = trees[i].unit_weight * trees[i].height * trees[i].thickness;
	}
}

void greedy_evaluate(struct Tree *tree) {
	tree->time = abs(tree->x-position.x)+abs(tree->y-position.y)+tree->thickness;
	tree->rate = ((float)tree->value)/tree->time;
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
	if (time+time_required <= time_limit) {
		return 1;
	}
	else {
		return 0;
	}
}

void navigate_to(struct Tree *tree) {
	while (tree->x > position.x && is_time_left(1) && tree->status) {
		printf("move right\n");
		position.x++;
		time++;
	}
	while (tree->x < position.x && is_time_left(1) && tree->status) {
		printf("move left\n");
		position.x--;
		time++;
	}
	while (tree->y > position.y && is_time_left(1) && tree->status) {
		printf("move up\n");
		position.y++;
		time++;
	}
	while (tree->y < position.y && is_time_left(1) && tree->status) {
		printf("move down\n");
		position.y--;
		time++;
	}
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

void domino_effect(int side, struct Tree *tree) {
	switch (side) {
		case 0:
			for (int i = 1; i < tree->height; ++i) {
				if (is_tree(tree->x, tree->y+i)) {
					struct Tree *tree_under = tree_at(tree->x, tree->y+i);
					if (tree->weight > tree_under->weight) {
						tree_under->status = 0;
						domino_effect(side, tree_under);
					}
					else {
						return;
					}
				}
			}
			break;
		case 1:
			for (int i = 1; i <= tree->height; ++i) {
				if (is_tree(tree->x+i, tree->y)) {
					struct Tree *tree_under = tree_at(tree->x+i, tree->y);
					if (tree->weight > tree_under->weight) {
						tree_under->status = 0;
						domino_effect(side, tree_under);
					}
					else {
						return;
					}
				}
			}
			break;
		case 2:
			for (int i = 1; i <= tree->height; ++i) {
				if (is_tree(tree->x, tree->y-i)) {
					struct Tree *tree_under = tree_at(tree->x, tree->y-i);
					if (tree->weight > tree_under->weight) {
						tree_under->status = 0;
						domino_effect(side, tree_under);
					}
					else {
						return;
					}
				}
			}
			break;
		case 3:
			for (int i = 1; i <= tree->height; ++i) {
				if (is_tree(tree->x-i, tree->y)) {
					struct Tree *tree_under = tree_at(tree->x-i, tree->y);
					if (tree->weight > tree_under->weight) {
						tree_under->status = 0;
						domino_effect(side, tree_under);
					}
					else {
						return;
					}
				}
			}
			break;
		default:
			printf("Internal error! Incorrect use of function domino_effect\n");
			break;
	}
}

int domino_value(int side, struct Tree *tree) {
	int value = 0;
	switch (side) {
		case 0:
			for (int i = 1; i <= tree->height; ++i) {
				if (is_tree(tree->x, tree->y+i)) {
					struct Tree *tree_under = tree_at(tree->x, tree->y+i);
					if (tree->weight > tree_under->weight) {
						value+=tree->value;
					}
					else {
						return value;
					}
				}
			}
			break;
		case 1:
			for (int i = 1; i <= tree->height; ++i) {
				if (is_tree(tree->x+i, tree->y)) {
					struct Tree *tree_under = tree_at(tree->x+i, tree->y);
					if (tree->weight > tree_under->weight) {
						value+=tree->value;
					}
					else {
						return value;
					}
				}
			}
			break;
		case 2:
			for (int i = 1; i <= tree->height; ++i) {
				if (is_tree(tree->x, tree->y-i)) {
					struct Tree *tree_under = tree_at(tree->x, tree->y-i);
					if (tree->weight > tree_under->weight) {
						value+=tree->value;
					}
					else {
						return value;
					}
				}
			}
			break;
		case 3:
			for (int i = 1; i <= tree->height; ++i) {
				if (is_tree(tree->x-i, tree->y)) {
					struct Tree *tree_under = tree_at(tree->x-i, tree->y);
					if (tree->weight > tree_under->weight) {
						value+=tree->value;
					}
					else {
						return value;
					}
				}
			}
			break;
		default:
			printf("Internal error! Incorrect use of function domino_value\n");
			break;
	}
	return value;
}

void cut(struct Tree *tree) {
	if (is_time_left(tree->thickness)) {
		int maxdir = 0;
		int max = 0;
		int temp = 0;
		for (int i = 0; i < 4; ++i) {
			temp = domino_value(i, tree);
			if (temp > max) {
				max = temp;
				maxdir = i;
			}
		}
		switch (maxdir) {
			case 0:
				printf("cut up\n");
				break;
			case 1:
				printf("cut right\n");
				break;
			case 2:
				printf("cut down\n");
				break;
			case 3:
				printf("cut left\n");
				break;
		}
		time += tree->thickness;
		tree->status = 0;
		domino_effect(maxdir, tree);
	}
}

void select(struct Tree *tree) {
	int maxdir = 0;
	int max = 0;
	int temp = 0;
	for (int i = 0; i < 4; ++i) {
		temp = domino_value(i, tree);
		if (temp > max) {
			max = temp;
			maxdir = i;
		}
	}
	time += tree->thickness;
	tree->status = 0;
	domino_effect(maxdir, tree);
}

struct Tree *closest_tree(struct node *list) {
	// return closest tree to current position in list
}

void greedy_navigate(struct node *list) {
	struct Tree *greedy_tree = closest_tree();
	navigate_to(greedy_tree);
	cut(greedy_tree);
}

struct node *greedy_add(struct node *list) {
	struct Tree *greedy_tree = max_value_tree();
	navigate_to(greedy_tree);
	if (is_time_left(tree->thickness)) {
		select(greedy_tree);
		list = insert_beginning(list, greedy_tree);
	}
	return list;
}

reset_trees(struct node *list) {
	// Reset status of all trees in list to 1
}

void greedy_approach(void) {
	position.x=0;
	position.y=0;
	int real_pos_x, real_pos_y, real_time;

	while (is_time_left(1)) {
		// Create Optimal List
		real_pos_x = position.x;
		real_pos_y = position.y;
		real_time = time;
		struct node *list;
		while (is_time_left(1)) {
			greedy_evaluate_all();
			list = greedy_add(list);
		}

		// Restore the setup
		position.x = real_pos_x;
		position.y = real_pos_y;
		time = real_time;
		reset_trees(list);
		// Reset domino trees too

		// Cut trees in closest greedy way
		while (list) {
			greedy_navigate(list);
		}
	}
}

// Linked List Implementation
struct node {
	struct Tree *data;
	struct node *next;
};

struct node *create_node(void) {
	struct node *newnode = (struct node*) malloc(sizeof(struct node));
	newnode->data=NULL;
	newnode->next=NULL;
	return newnode;
}

struct node *add_to_empty_list(struct node *head, struct Tree *data) {
	struct node *newnode;
	newnode = create_node();
	newnode->data = data;
	head = newnode;
	newnode->next = head;
	return head;
}

struct node *insert_beginning(struct node *head, struct Tree *data) {
	if (head == NULL) {
		head = add_to_empty_list(head, data);
	}
	else {
		struct node *last = head;
		while (last->next != head) {
			last = last->next;
		}
		struct node *newnode = create_node();
		newnode->data = data;
		newnode->next = head;
		head = newnode;
		last->next = newnode;
	}
	return head;
}

struct Tree *value_at(struct node *head, int pos) {
	if (head == NULL) {
		return NULL;
	}
	else {
		struct node *currentnode = head;
		for (int i = 0; i < pos; ++i) {
			if (currentnode->next == head) {
				return NULL;
			}
			else {
				currentnode = currentnode->next;
			}
		}
		return currentnode->data;
	}
}

struct node *delete_beginning(struct node *head) {
	if (head == NULL) {
		printf("Cannot delete, list is empty!\n\n");
	}
	else {
		struct node *delete;
		delete = head;
		if (delete->next == head) {
			head = NULL;
		}
		else {
			struct node *last;
			last = head;
			while (last->next != head) {
				last = last->next;
			}
			head = delete->next;
			last->next = delete->next;
		}
		free(delete);
	}
	return head;
}

struct node *delete_from(struct node *head, int pos) {
	if (head == NULL) {
		printf("Cannot delete, list is empty!\n\n");
	}
	else {
		struct node *delete;
		delete = head;
		if (delete->next == head) {
			if (pos == 0) {
				head = NULL;
				free(delete);
			}
			else {
				printf("Invalid position!\n\n");
			}
		}
		else {
			if (pos < 0) {
				printf("Invalid position!\n\n");
			}
			else if (pos == 0) {
				head = delete_beginning(head);
			}
			else {
				struct node *prev;
				for (int i = 0; i < pos; ++i) {
					prev = delete;
					delete = delete->next;
					if (delete == head) {
						printf("Invalid position!\n\n");
						return head;
					}
				}
				prev->next = delete->next;
				free(delete);
			}
		}
	}
	return head;
}