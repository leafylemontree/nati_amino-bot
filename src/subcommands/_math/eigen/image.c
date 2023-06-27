#include "libmatrix.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define NODES 32

COLOR *COLOR_create(double r, double g, double b){
	COLOR *col = (COLOR *)malloc(sizeof(COLOR));
	col->r = r;
	col->g = g;
	col->b = b;
	return col;
}

void COLOR_free(COLOR *col){
	if(col != NULL) free(col);
}

TREE *TREE_init(double r, double g, double b){
	TREE  *tree = (TREE *)malloc(sizeof(TREE));
	tree->color.r = r;
	tree->color.g = g;
	tree->color.b = b;
	tree->weight  = 1;
	tree->indent  = 0;
	tree->done    = 0;
	tree->left    = NULL;
	tree->right   = NULL;
	tree->up      = NULL;
	return tree;
}

void TREE_free(TREE *tree){
	//printf("Now: %p\n", tree);
	if(tree == NULL) return;
	//printf("L: %p\n", tree->left);
	//printf("R: %p\n", tree->right);
	if(tree->left  != NULL) TREE_free(tree->left);
	if(tree->right != NULL) TREE_free(tree->right);
	free(tree);
	return;
}


double COLOR_difference(double r1, double g1, double b1, double w1, double r2, double g2, double b2, double w2){
	double rd = (r2 - r1);
	double gd = (g2 - g1);
	double bd = (b2 - b1);
	double wd = (w2 - w1);
	
	double  d = rd*rd + gd*gd + bd*bd + wd*wd;
	return sqrt(d);
}

double COLOR_delta(double r, double g, double b){
	return sqrt(r*r + g*g + b*b);
}

void TREE_inserNode(TREE *tree, double r, double g, double b){
	double d1;
	double d2;

	TREE *now  = tree;
	TREE *prev = NULL;
	TREE *node = NULL;
	int   indent = 0;
	double d   = 0;
	
	do {
		d1 = COLOR_delta(now->color.r, now->color.g, now->color.b);
		d2 = COLOR_delta(r, g, b);

		if(fabs(d2 - d1) < 5) {
			prev = now;
			now->weight += 1;

			//d = fabs(d2 - d1)/(d2 + 1);
			//d = 1/(1 + sqrt(pow(r - now->color.r, 2) + pow(g - now->color.g, 2) + pow(b - now->color.b, 2) + pow(1 - now->weight, 2)));

			//d = 1/ (1+ fabs(d2 - d1));
			d = 1;	

			//now->color.r = (now->color.r * now->weight + r * d) / (now->weight + d);
			//now->color.g = (now->color.g * now->weight + g * d) / (now->weight + d);
			//now->color.b = (now->color.b * now->weight + b * d) / (now->weight + d);
			now->weight  = now->weight + d;
			break;
		} else if (d1 > d2){
			prev = now;
			now  = now->left;
			if(now == NULL){
				prev->left 		= TREE_init(r, g, b);
				prev->left->indent 	= prev->indent + 1;
				prev->left->up 	   	= prev;
				break;
			};
			indent++;

		} else if(d1 < d2){
			prev = now;
			now  = now->right;
			if(now == NULL){
				prev->right 		= TREE_init(r, g, b);
				prev->right->indent 	= prev->indent + 1;
				prev->right->up		= prev;
				break;
			};
			indent++;
		};

	} while(now != NULL);

	return;
}

void TREE_indent_filePrint(TREE *tree, FILE *f, int *c){
	//printf("Tree pointer %p\n", tree);
	if(tree == NULL) return;
	if(tree->indent > 40)return;
	//printf("No return\n");
	fprintf(f, "\n");
	for(int i = 0; i < *c; i++) fprintf(f, "  ");
	fprintf(f, "NODE r: %.2lf g: %.2lf b: %.2lf w: %.2lf i: %i\th: %2X%2X%2X\t", tree->color.r, tree->color.g, tree->color.b, tree->weight, tree->indent, (int)tree->color.r, (int)tree->color.g, (int)tree->color.b);
	*c = (*c) + 1;

	if (tree->left != NULL){
		fprintf(f, "LEFT -> ");
		TREE_indent_filePrint(tree->left, f, c);
	}
	if (tree->right != NULL){
		fprintf(f, "RIGHT -> ");
		TREE_indent_filePrint(tree->right, f, c);
	};

	*c = (*c) - 1;
	return;
}

void TREE_filePrint(TREE *tree, FILE *f){
	int c = 0;
	TREE_indent_filePrint(tree, f, &c);
}

TREE *TREE_color_average(int w, int h, unsigned char *r, unsigned char *g, unsigned char *b){
	unsigned long ra = 0;
	unsigned long ga = 0;
	unsigned long ba = 0;
	unsigned long e  = w*h;

	for(int x = 0; x < w; x++){
		for(int y = 0; y < h; y++){
			ra += r[x + y*w];
			ga += g[x + y*w];
			ba += b[x + y*w];
		}
	}
	printf("r: %li\tg: %li\tb: %li\ne: %li\n", ra, ga, ba, e);
	
	return TREE_init(
		ra / (double)e,			
		ga / (double)e,			
		ba / (double)e
	);
}

TREE *TREE_branchCut(TREE *tree){
	if(tree == NULL) return NULL;
	printf("Creating branch: %p\n", tree);
	TREE *branch = TREE_init(tree->color.r, tree->color.g, tree->color.b);
	branch->weight  = tree->weight;
	branch->left	= tree->left;
	branch->right	= tree->right;
	branch->up	= NULL;
	branch->indent  = 0;
	return branch;
}


void TREE_quantize(TREE *tree){
	if(tree == NULL) return;
	//printf("Tree quantize\n");
	TREE *past  = NULL;
	TREE *now   = tree;

	int direction = 0; // -1: going up	1: going down

	while(1){
		//printf("prev: %p\nnow: %p\n\tleft: %p\tright: %p\n\tup: %p\nDir: %i\n", past, now, now->left, now->right, now->up, direction);
		if(now->up == NULL && now->left == NULL && now->right == NULL){
			return;
		};

		if(past == NULL && direction != 0){
			return;
		}

		if(now->up == now->left || now->up == now->right){
			return;
		}

		if(now == now->left || now == now->right){
			return;
		}

		if(past == now->left || past == now->right){
			return;
		}

		//printf("No easy exit\n");

		if(now->left != NULL){
			//printf("Left branch: %p\n", now->left);
			past 		= now;
			now  		= now->left;
			direction 	= 1;
		} else if(now->right != NULL){
			//printf("Right branch: %p\n", now->right);
			past 		= now;
			now  		= now->right;
			direction 	= 1;
		} else if(now->left == NULL && now->right == NULL && now != NULL && past != NULL){
			//printf("Merge childs with parent\n");
			past->color.r = ((past->color.r * past->weight) + (now->color.r * now->weight)) / (past->weight + now->weight);
			past->color.g = ((past->color.g * past->weight) + (now->color.g * now->weight)) / (past->weight + now->weight);
			past->color.b = ((past->color.b * past->weight) + (now->color.b * now->weight)) / (past->weight + now->weight);
			past->weight  = past->weight    + now->weight;

			if(past->left  == now)  past->left  = NULL;
			if(past->right == now)  past->right = NULL;
			
			//printf("Free %p\n", now);
			free(now);
			now  = past;
			past = now->up;
		} else {
			break;
		}
	}
	return;
}

int flagSeparator(int i, int j){
	int s = (((i | (i << 4)) >> j) & 0x1);
	printf("%i\t%i\t%i\n", i, j, s);
	return s;
}


TREE *TREE_subTree(TREE *tree, int i){
	//printf("Branch: %i\n", i);
	TREE *now  = tree;
	TREE *prev = NULL;
	int s = 0;
	int k = 0;

	for(int j = 0; j < 5; j++){
		if(j == 4) k = 3;
		else       k = j;
		s = flagSeparator(i, k);

		if(now->left != NULL && s == 0){
			prev = now;
			now  = now->left;
		} else if (now->right != NULL && s == 0){
			prev = now;
			now  = now->right;
		} else if(now->right != NULL && s == 1){
			prev = now;
			now  = now->right;
		} else if (now->left != NULL && s == 1){
			prev = now;
			now  = now->left;
		} else {
			if(prev != NULL){
				if (prev->left  == now)  prev->left  = NULL;
				if (prev->right == now)  prev->right = NULL;
			};
		};
	}
	TREE *newTree = TREE_branchCut(now);
	return newTree;
}

void TREE_printHex(TREE *tree, FILE *f){
	fprintf(f, "- #%2x%2x%2x\tr: %.2lf\tg: %.2lf\tb: %.2lf\tw: %.2lf\n", (unsigned char)tree->color.r, (unsigned char)tree->color.g, (unsigned char)tree->color.b, tree->color.r, tree->color.g, tree->color.b, tree->weight);
}


void TREE_toColor(TREE *tree, COLOR c[], int size){
	printf("Copying...\n");
	for(int i = 0; i < size; i++){
		if(c[i].set == 1) continue;
		c[i].r = tree->color.r;
		c[i].g = tree->color.g;
		c[i].b = tree->color.b;
		c[i].weight = tree->weight;
		c[i].set = 1;
		break;
	};

	if(tree->left != NULL){
		printf("Going left\n");
		TREE_toColor(tree->left, c, size);
	}
	
	if (tree->right != NULL){
		printf("Going right\n");
		TREE_toColor(tree->right, c, size);
	}
	
}


char *image_tree(int w, int h, unsigned char *r, unsigned char *g, unsigned char *b){
	TREE *tree = TREE_color_average(w, h, r, g, b);
	printf("w: %i\nh: %i\n", w,h);
	printf("Average:\n\tr: %.2lf\n\tg: %.2lf\n\tb: %.2lf\n", tree->color.r, tree->color.g, tree->color.b);
	COLOR pr;
	pr.r = tree->color.r;
	pr.g = tree->color.g;
	pr.b = tree->color.b;

	for(int x = 0; x < w; x++){
		for(int y = 0; y < h; y++){
			TREE_inserNode(tree, r[x + y*w], g[x + y*w], b[x + y*w]);
		}
	}

	COLOR c[NODES];
	for(int i = 0; i < NODES; i++) c[i].set = 0;
	TREE_toColor(tree, c, NODES);
	
	char *s;
	unsigned long l;
	FILE *buffer = open_memstream(&s, &l);
	fprintf(buffer, "%02X%02X%02X\n", (unsigned char)pr.r, (unsigned char)pr.g, (unsigned char)pr.b);
	for(int i = 0; i < NODES; i++) fprintf(buffer, "%02X%02X%02X\t%.2lf\n", (unsigned char)c[i].r, (unsigned char)c[i].g, (unsigned char)c[i].b, c[i].weight);

	fflush(buffer);
	fclose(buffer);
	printf("%s\n", s);
	return s;
}


