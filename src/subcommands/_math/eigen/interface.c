#include "libmatrix.h"
#include <stdio.h>
#include <stdlib.h>

char *eigen_image(int width, int height, unsigned char *data){
	if(width != height) return NULL;

	MATRIX *m = MATRIX_init(width, height, NULL, 1);
	for(int x = 0; x < width; x++){
		for(int y = 0; y < height; y++){
			MATRIX_set(m, x, y, (data[x + y*(width)]/(double)256), 0);
		};
	};
	char *s = MATRIX_print(m);
	printf("Matrix:\n%s\n", s);
	free(s);
	
	MATRIX_lambda(m);
	printf("Matrix lambda\n");
	POLY *p = MATRIX_determinant(m);
	printf("Matrix determinant\n");
	VECTOR *v = POLY_zeroes(p);
	printf("Matrix eigenvalues\n");
	s = VECTOR_print(v);

	MATRIX_free(m);
	POLY_free(p);
	VECTOR_free(v);
	return s;
}
