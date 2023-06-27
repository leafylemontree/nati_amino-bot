#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "libmatrix.h"

POLY *POLY_init(int grade, char *label, double *values, char freeLabel, char freeValues){
	POLY *r = (POLY *)malloc(sizeof(POLY));

	if(values == NULL){
		r->values 	= (double *)malloc(sizeof(double) * (grade + 1));
		for(int i = 0; i <= grade; i++) r->values[i] = 0;
		r->freeValues 	= 1;
	} else {
		r->values	= values;
		r->freeValues 	= freeValues;
	};

	r->grade = grade;
	r->label = label;
	r->freeLabel = freeLabel;
	return r;
}

POLY *POLY_copy(POLY *origin){
	POLY *final 		= (POLY *)malloc(sizeof(POLY));
	final->values 		= (double *)malloc((origin->grade + 1) * sizeof(double));
	final->label 		= (char *)malloc(strlen(origin->label) + 1);

	strcpy(final->label, origin->label);
	for(int i = 0; i <= origin->grade; i++) final->values[i] = origin->values[i];

	final->freeLabel 	= 1;
	final->freeValues 	= 1;
	final->grade 		= origin->grade;
	return final;
}

void POLY_scalar(POLY *poly, double s){
	for(int i = 0; i <= poly->grade; i++)	poly->values[i] = poly->values[i] * s;
	return;
}

POLY *POLY_mul(POLY *a, POLY *b){
	POLY *c = POLY_init(a->grade + b->grade, a->label, NULL, 0, 1);
	
	for(int i = 0; i <= a->grade; i++){
		for(int j = 0; j <= b->grade; j++){
			c->values[i+j] += a->values[i] * b->values[j];
		};
	};

	return c;
}


DIVRESULT *DIVRESULT_init(POLY *p, POLY *r){
	DIVRESULT *d 	= (DIVRESULT *)malloc(sizeof(DIVRESULT));
	d->p		= POLY_copy(p);
	d->r		= POLY_copy(r);
	return d;
}

void DIVRESULT_free(DIVRESULT *d){
	if(d    == NULL)	return;
	if(d->p != NULL)	POLY_free(d->p);
	if(d->r != NULL)	POLY_free(d->r);
	free(d);
}

DIVRESULT *POLY_div(POLY *p1, POLY *p2){
	if(p1 == NULL || p2 == NULL) return NULL;
	int deltaGrade = p1->grade - p2->grade;

	if(deltaGrade < 0) 	return NULL;
	if(p2->grade > 2)	return NULL;

	POLY *p1c = POLY_copy(p1);
	POLY *p2c = POLY_copy(p2);

	double c = 0;
	POLY *pf = POLY_init(deltaGrade, p1->label, NULL, 0, 1);
	POLY *r  = POLY_init(1         , p1->label, NULL, 0, 1);

	for(int i = p1->grade; i >= p2->grade; i--){

		if(p1c->values[i] 	  == 0)     continue;
		if(p2c->values[p2->grade] == 0)     continue;
		c = p1c->values[i] / (double) p2c->values[p2c->grade];
		pf->values[i - p2c->grade] = c;

		for(int j = p2->grade; j >= 0; j--){
			if(p2c->values[j] == 0) continue;
			p1c->values[i + j - p2c->grade] -= c * p2c->values[j];
		};

	};

	r->values[0] = p1c->values[0];
	r->values[1] = p1c->values[1];

	POLY_free(p1c);
	POLY_free(p2c);

	DIVRESULT *d = DIVRESULT_init(pf, r);
	POLY_free(pf);
	POLY_free(r);
	return d;
}

char *POLY_print(POLY *p){
	char *buffer;
	unsigned long int l;
	FILE *fl	= open_memstream(&buffer, &l);

	for(int i = 0; i <= p->grade; i++){
		
		switch(i){
			case 0:	
				fprintf(fl, "\t -   \t = %lf\n", p->values[i]);
				break;

			case 1:	
				fprintf(fl, "\t - %s\t = %lf\n", p->label, p->values[i]);
				break;

			default:	
				fprintf(fl, "\t - %s↑%i\t = %lf\n", p->label, i, p->values[i]);
				break;
		}
	
	}

	fflush(fl);
	fclose(fl);
	return buffer;
}

char *POLY_repr(POLY *p){
	char *buffer;
	unsigned long int l;
	FILE *fl	= open_memstream(&buffer, &l);
	int printed = 0;
	
	for(int i = p->grade; i >= 0; i--){
		if(p->values[i] == 0 && i != 0) continue;
		if (i == 0 && p->values[i] == 0 && printed == 1){
			continue;
		} else if(i != p->grade && printed == 1){
			fprintf(fl, " ");
			if(p->values[i] < 0) fprintf(fl, "-");
			else		     fprintf(fl, "+");
			fprintf(fl, " ");
		} else {
			if(p->values[i] < 0) fprintf(fl, "-");
		};

		printed = 1;
		if(i != 0 && p->values[i] != 1){
			fprintf(fl, "%.4lf", fabs(p->values[i]));
		} else if (i == 0){
			fprintf(fl, "%.4lf", fabs(p->values[i]));
		}
		switch(i){
			case 0:

				break;
			case 1:

				fprintf(fl, "%s", p->label);
				break;
			default:
				fprintf(fl, "%s^%i", p->label, i);
				break;
		};
	};

	fflush(fl);
	fclose(fl);
	return buffer;
}

// c = a + b
POLY *POLY_add(POLY *a, POLY *b){
	int grade = 0;
	if (a->grade > b->grade) grade = a->grade;
	else			 grade = b->grade;

	POLY *c = POLY_init(grade, a->label, NULL, 0, 1);
	for(int i = 0; i <= grade; i++) c->values[i] = a->values[i] + b->values[i];

	return c;
}

double POLY_eval(POLY *p, double x){
	double y = p->values[0];
	double xp= 1;
	for(int i = 1; i <= p->grade; i++){
		xp = xp * x;
		y += xp * p->values[i];
	};
	return y;
}

POLY *POLY_derivate(POLY *p){
	int newGrade = (p->grade) - 1;
	if(newGrade < 0) return NULL;

	POLY *pd = POLY_init(newGrade, p->label, NULL, 0, 1);
	for(int i = 1; i <= p->grade; i++){
		pd->values[i-1] = p->values[i] * i;
	};

	return pd;
}

POLY *POLY_integrate(POLY *p){
	int newGrade = (p->grade) + 1;

	POLY *pi = POLY_init(newGrade, p->label, NULL, 0, 1);
	for(int i = 1; i <= pi->grade; i++){
		pi->values[i] = p->values[i-1] / (double) i;
	};
	pi->values[0] = 0;
	return pi;
}

void POLY_free(POLY *p){
	if(p == NULL) return;
	if(p->freeLabel  == 1 && p->label  != NULL) free(p->label);
	if(p->freeValues == 1 && p->values != NULL) free(p->values);
	free(p);
}




int __poly_div_zero(POLY *p){
	return (p->values[0] == 0);
}

double __discriminant(double a, double b, double c){
	return b*b - 4*a*c;
}

DIVRESULT *__poly_2_roots(POLY *p){
	if(p->grade != 2) return NULL;

	double a = p->values[2];
	double b = p->values[1];
	double c = p->values[0];
	double d = __discriminant(a, b, c);

	POLY *r  = POLY_init(1, "i", NULL, 0, 1);
	if(d < 0){
		d = fabs(d);
		r->values[0] = 0;
		r->values[1] = sqrt(d);
	} else {
		r->values[0] = sqrt(d);
	};
	
	POLY *rA = POLY_copy(r);
	POLY *rB = POLY_copy(r);
	POLY_scalar(rB, -1);

	rA->values[0] -= b;
	rB->values[0] -= b;
	POLY_scalar(rA, 0.5);
	POLY_scalar(rB, 0.5);

	DIVRESULT *dr = DIVRESULT_init(rA, rB);
	POLY_free(r);
	POLY_free(rA);
	POLY_free(rB);
	return dr;
}

double newton_raphson_raw(POLY *p, POLY *pd){
	double x = 1;
	double a = 0;
	double b = 0;
	for(int i = 0; i < 100000; i++){
		a = POLY_eval(p,  x);
		b = POLY_eval(pd, x);

		if(b == 0) break;
		if(a == 0) break;
		x = x - (a/b);
	};
	return x;
}


int newton_test(POLY *p){
	POLY *pd  = POLY_derivate(p);
	POLY *pd2 = POLY_derivate(pd);
	double x  = newton_raphson_raw(pd, pd2);

	double y  = POLY_eval(p, x);

	int    t  = 1;
	if((p->values[p->grade] * y) > 1){
		t = -1;
	};
	POLY_free(pd);
	POLY_free(pd2);
	return t;
}

double POLY_newton(POLY *p){
	//int    t    = newton_test(p);

	POLY *f  = POLY_copy(p);
	POLY *fd = POLY_derivate(p);

	double x    = newton_raphson_raw(f, fd);

	POLY_free(f);
	POLY_free(fd);
	return x;
}
