#include <stdio.h>
#include <stdlib.h>
#include "libmatrix.h"

VECTOR *VECTOR_init(int rows){
	VECTOR *v = (VECTOR *)malloc(sizeof(VECTOR));
	v->values = (POLY **)malloc(sizeof(POLY *) * rows);
	v->rows	  = rows;
	for(int i = 0; i < rows; i++) v->values[i] = NULL;
	return v;
}


int VECTOR_appendPOLY(VECTOR *v, POLY *p){
	for(int i = 0; i < v->rows; i++){
		if (v->values[i] != NULL) continue;
		v->values[i] = POLY_copy(p);
		return i;
	};
	return -1;
}

int VECTOR_appendScalar(VECTOR *v, double f){
	for(int i = 0; i < v->rows; i++){
		if (v->values[i] != NULL) continue;
		v->values[i] = POLY_init(0, "x", NULL, 0, 1);
		v->values[i]->values[0] = f;
		return i;
	};
	return -1;
}

char *VECTOR_print(VECTOR *v){
	char *buffer;
	unsigned long int l;
	FILE *fl	= open_memstream(&buffer, &l);
	
	char *s;
	fprintf(fl, "[");
	for(int i = 0; i < v->rows; i++){
		if(v->values[i] != NULL && i != 0) fprintf(fl, ", ");
		if(v->values[i] == NULL) continue;
		s = POLY_repr(v->values[i]);
		fprintf(fl, "%s", s);
		free(s);
	}
	fprintf(fl, "]");

	fflush(fl);
	fclose(fl);
	return buffer;
}

void VECTOR_free(VECTOR *v){
	for(int i = 0; i < v->rows; i++){
		if(v->values[i] == NULL) continue;
		POLY_free(v->values[i]);
	};
	free(v->values);
	free(v);
}

VECTOR *POLY_zeroes(POLY *p){
	VECTOR *v = VECTOR_init(p->grade);
	
	POLY *pa = POLY_init(1, "x", NULL, 0, 1);
	POLY *pc = POLY_copy(p);
	DIVRESULT *dr = NULL;

	// x = 0
	pa->values[0] = 0;
	pa->values[1] = 1;
	while(1){
		if(! __poly_div_zero(pc)) break;
		VECTOR_appendScalar(v, 0);

		dr = POLY_div(pc, pa);
		if(dr == NULL){
			break;
		};

		POLY_free(pc);
		pc = POLY_copy(dr->p);
		
		DIVRESULT_free(dr);
	};

	// Newton-Rhapson
	
	double nr = 0;
	while(1){
		if(pc->grade <= 2) break;

		nr = POLY_newton(pc);

		VECTOR_appendScalar(v, nr);
		pa->values[0] = -nr;
		pa->values[1] = 1;
		dr = POLY_div(pc, pa);
		if(dr == NULL){
			break;
		};

		POLY_free(pc);
		pc = POLY_copy(dr->p);
		DIVRESULT_free(dr);
	}
	
	// Quadratic formula
	
	if(pc->grade == 2){
		dr = __poly_2_roots(pc);
		VECTOR_appendPOLY(v, dr->p);
		VECTOR_appendPOLY(v, dr->r);
		DIVRESULT_free(dr);
	};

	POLY_free(pc);
	POLY_free(pa);
	return v;
}


