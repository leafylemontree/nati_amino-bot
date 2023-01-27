#include <stdlib.h>
#include <stdio.h>

float predict(int *registries, int len){
	float *coef = (float *)malloc(sizeof(float) * len);
		
	float eval = 0;		// Evaluates all terms before the current one
	int   mult = 0;
	int   fact = 1;

	for(int r = 0; r < len; r++) fprintf(stdout, "\t%i %i\n", r, registries[r]);

	for(int a = 0; a < len; a++) coef[a] = 0;

	for(int i = 0; i < len; i++){

		eval = registries[0];
		mult = 1;

		for(int j = 0; j < i-1; j++){
			mult *= i-j;
			eval += mult * coef[j+1];
		};
		
		if (i > 0) {
			fact *= i;
			coef[i] = (registries[i] - eval)/(float)fact;
		} else {
			coef[i] = registries[0];
		};
	};

	int guess = len + 1;

	fact = 1;
	eval = 0;
	for(int c = 0; c < len; c++){
		if (c > 0) {
			fact *= guess - c;
			eval += fact * coef[c];
		} else {
			eval += coef[c];
		};
	};

	free(coef);
	return eval;
}

