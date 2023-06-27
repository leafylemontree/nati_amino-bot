#include <stdio.h>
#include <stdlib.h>
#include "libmatrix.h"

MATRIX *MATRIX_init(int rows, int columns, POLY ***values, int freeValues){
	MATRIX *m = (MATRIX *)malloc(sizeof(MATRIX));

	if(values == NULL){
		m->values = (POLY ***)malloc(sizeof(POLY *) * rows);
		for(int i = 0; i < rows; i++){
			m->values[i] = (POLY **)malloc(sizeof(POLY *) * columns);
			for(int j = 0; j < columns; j++){
				m->values[i][j] = POLY_init(0, "l", NULL, 0, 1);
			}
		}
		m->freeValues 	= 1;
	} else {
		m->values	= values;
		m->freeValues 	= freeValues;
	};

	m->rows 	= rows;
	m->columns 	= columns;
	return m;
}

MATRIX *MATRIX_copy(MATRIX *m1){
	MATRIX *m2 = MATRIX_init(m1->rows, m1->columns, NULL, 1);
	m2->values = (POLY ***)malloc(sizeof(POLY *) * m2->rows);
	for(int i = 0; i < m2->rows; i++){
		m2->values[i] = (POLY **)malloc(sizeof(POLY *) * m2->columns);
		for(int j = 0; j < m2->columns; j++){
			m2->values[i][j] = POLY_copy(m1->values[i][j]);
		}
	}
	m2->freeValues 	= 1;
	return m2;
}

MATRIX *MATRIX_sub(MATRIX *m1, int row, int column){
	MATRIX *s = MATRIX_init((m1->rows)-1, (m1->columns)-1, NULL, 1);

	int n = 0; // rows
	int m = 0; // columns

	for(int y = 0; y < m1->rows; y++){
		if(y == row)				continue;
		m = 0;
		for(int x = 0; x < m1->columns; x++){
			if(x == column)			continue;
			POLY_free(s->values[n][m]);
			s->values[n][m]	= POLY_copy(m1->values[y][x]);
			m++;
		};
		n++;
	}
	return s;
}

int MATRIX_set(MATRIX *m, int row, int column, double value, int grade){
	if(row 	  >= m->rows	) 			return -1;
	if(column >= m->columns	) 			return -1;
	if(grade > m->values[row][column]->grade) 	return -1;

	m->values[row][column]->values[grade] = value;
	return 0;
}

void MATRIX_scalar(MATRIX *m, double value){
	for(int r = 0; r < m->rows; r++){
		for(int c = 0; c < m->columns; c++){
			POLY_scalar(m->values[r][c], value);
		}
	}
	return;
}

void MATRIX_add(MATRIX *m1, MATRIX *m2){
	POLY *p;
	POLY *p1;
	POLY *p2;

	if(m1->rows 	!= m2->rows) 	return;
	if(m1->columns 	!= m2->columns) return;

	for(int r = 0; r < m1->rows; r++){
		for(int c = 0; c < m1->columns; c++){
			p1 = m1->values[r][c];
			p2 = m2->values[r][c];

			p = POLY_add(p1, p2);
			POLY_free(p1);
			m1->values[r][c] = p;
		}
	}
	return;
}

// m3 = m1 * m2
MATRIX *MATRIX_mul(MATRIX *m1, MATRIX *m2){
	POLY *p1;	// Polynom 1
	POLY *p2;	// POlynom 2
	POLY *p3;	// POlynom 3
	POLY *pm;	// Temporal polynom
	POLY *pt;	// Temporal polynom
	POLY *pf;	// accumulator

	if(m1->rows 	!= m2->columns) return NULL;
	MATRIX *m3 = MATRIX_init(m1->rows, m2->columns, NULL, 1);
	//printf("rows: %i\tcolumns: %i\n", m2->rows, m1->columns);

	for(int y = 0; y < m1->rows; y++){
		for(int x = 0; x < m2->columns; x++){
			
			p3 = m3->values[y][x];
			pf = POLY_init(0, "L", NULL, 0, 1);

			for(int c = 0; c < m1->columns; c++){
				p1 = m1->values[y][c];
				p2 = m2->values[c][x];

				pm = POLY_mul(p1, p2);
				//printf("x: %i\ty: %i\tc: %i\n\n",x,y,c);
				pt = POLY_add(pm, pf);
				POLY_free(pm);
				POLY_free(pf);
				pf = POLY_copy(pt);
				POLY_free(pt);
			};

			POLY_free(p3);
			m3->values[y][x] = POLY_copy(pf);
			POLY_free(pf);
		}
	}
	return m3;
}

void MATRIX_lambda(MATRIX *m){
	if(m->rows != m->columns) return;

	POLY *l = POLY_init(1, "L", NULL, 0, 1);
	l->values[1] = -1;
	l->values[0] = 0;
	POLY *p;


	for(int r = 0; r < m->rows; r++){
		p = POLY_add(m->values[r][r], l);
		POLY_free(m->values[r][r]);
		m->values[r][r] = p;
	}
	POLY_free(l);
	return;
}

char *MATRIX_print(MATRIX *m){
	char *buffer;
	unsigned long int l;
	FILE *fl = open_memstream(&buffer, &l);
	char *s;
	
	fprintf(fl, "{\n");
	for(int r = 0; r < m->rows; r++){
		for(int c = 0; c < m->columns; c++){
			s = POLY_repr(m->values[r][c]);
			fprintf(fl, "\t\t%s", s);
			free(s);
		};
		fprintf(fl, "\n");
	};
	fprintf(fl, "}\n");

	fflush(fl);
	fclose(fl);
	return buffer;
}



void MATRIX_free(MATRIX *m){
	for(int r = 0; r < m->rows; r++){
		for(int c = 0; c < m->columns; c++){
			POLY_free(m->values[r][c]);
		};
		free(m->values[r]);
	};
	free(m->values);
	free(m);
}


POLY * __determinant_2_2(MATRIX *m){
	POLY *p1  = m->values[0][0];
	POLY *p2  = m->values[1][1];
	POLY *p3  = m->values[1][0];
	POLY *p4  = m->values[0][1];

	POLY *p12 = POLY_mul(p1, p2);
	POLY *p34 = POLY_mul(p3, p4);

	POLY_scalar(p34, -1);
	POLY *f	  = POLY_add(p12, p34);

	POLY_free(p12);
	POLY_free(p34);
	f->label = "l";
	return f;
}

POLY *MATRIX_determinant(MATRIX *m){
	int rows 	= m->rows;
	int columns	= m->columns;

	if(rows != columns) return NULL;

	POLY *det	= NULL;
	MATRIX *sub_m	= NULL;

	if(rows == 2 && columns == 2){
		det 		= __determinant_2_2(m);
		return det;
	};
	
	det = POLY_init(0, "l", NULL, 0, 1);
	POLY *pA; // Acumulator
	POLY *pB; // Acumulator
	POLY *pN; // Now

	for(int r = 0; r < m->columns; r++){
		sub_m	= MATRIX_sub(m, 0, r);
		pN 	= MATRIX_determinant(sub_m);

		if((r & 0x1) == 1)	POLY_scalar(pN, -1);

		pA = POLY_mul(m->values[0][r], pN);
		POLY_free(pN);

		pB = det;
		det = POLY_add(pB, pA);

		POLY_free(pB);
		POLY_free(pA);
		MATRIX_free(sub_m);
	};

	return det;
}

