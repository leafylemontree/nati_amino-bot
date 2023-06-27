#include <stdio.h>

typedef struct {
	int 	grade;
	char   *label;
	double *values;

	char freeLabel;
	char freeValues;
} POLY; 

typedef struct {
	POLY *p;
	POLY *r;
} DIVRESULT;


POLY *POLY_init(int grade, char *label, double *values, char freeLabel, char freeValues);
POLY *POLY_copy(POLY *origin);
void POLY_scalar(POLY *poly, double s);
POLY *POLY_mul(POLY *a, POLY *b);
DIVRESULT *POLY_div(POLY *p1, POLY *p2);
POLY *POLY_add(POLY *a, POLY *b);
char *POLY_print(POLY *p);
char *POLY_repr(POLY *p);
double POLY_eval(POLY *p, double x);
POLY *POLY_derivate(POLY *p);
POLY *POLY_integrate(POLY *p);
void POLY_free(POLY *p);
DIVRESULT *DIVRESULT_init(POLY *p, POLY *r);
void DIVRESULT_free(DIVRESULT *d);
double POLY_newton(POLY *p);

int __poly_div_zero(POLY *p);
DIVRESULT *__poly_2_roots(POLY *p);

typedef struct {
	int	rows;
	int	columns;
	POLY ***values;
	char	freeValues;
} MATRIX;


MATRIX *MATRIX_init(int rows, int columns, POLY ***values, int freeValues);
MATRIX *MATRIX_copy(MATRIX *m);
MATRIX *MATRIX_sub(MATRIX *m, int row, int column);
int MATRIX_set(MATRIX *m, int row, int column, double value, int grade);
void MATRIX_scalar(MATRIX *m, double value);
void MATRIX_add(MATRIX *m1, MATRIX *m2);
MATRIX *MATRIX_mul(MATRIX *m1, MATRIX *m2);
void MATRIX_lambda(MATRIX *m);
char *MATRIX_print(MATRIX *m);
void MATRIX_free(MATRIX *m);
POLY *MATRIX_determinant(MATRIX *m);

typedef struct {
	int rows;
	POLY **values;
} VECTOR;

VECTOR *VECTOR_init(int rows);
int VECTOR_appendPOLY(VECTOR *v, POLY *p);
int VECTOR_appendScalar(VECTOR *v, double f);
char *VECTOR_print(VECTOR *v);
void VECTOR_free(VECTOR *v);
VECTOR *POLY_zeroes(POLY *p);

char *eigen_image(int width, int height, unsigned char *data);


typedef struct {
	double r;
	double g;
	double b;
	double weight;
	int set;
} COLOR;

typedef struct _tree{
	COLOR color;
	double weight;
	int indent;
	int done;
	
	struct _tree *left;
	struct _tree *right;
	struct _tree *up;
} TREE;


void COLOR_free(COLOR *col);
COLOR *COLOR_create(double r, double g, double b);
TREE *TREE_init(double r, double g, double b);
void TREE_free(TREE *tree);
double COLOR_difference(double r1, double g1, double b1, double w1, double r2, double g2, double b2, double w2);
double COLOR_delta(double r, double g, double b);
void TREE_inserNode(TREE *tree, double r, double g, double b);
void TREE_indent_filePrint(TREE *tree, FILE *f, int *c);
void TREE_filePrint(TREE *tree, FILE *f);
TREE *TREE_color_average(int w, int h, unsigned char *r, unsigned char *g, unsigned char *b);
char *image_tree(int w, int h, unsigned char *r, unsigned char *g, unsigned char *b);
void TREE_quantize(TREE *tree);
TREE *TREE_branchCut(TREE *tree);
TREE *TREE_subTree(TREE *tree, int i);
void TREE_printHex(TREE *tree, FILE *f);
