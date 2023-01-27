#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

double rate(char *text, int len){
	int   		mt = (len >> 3) + 1;
	unsigned char  *mr = malloc(mt * 8);

	printf("%i %i\n", len, mt);

	// copy input to matrix and add padding
	for(int i = 0; i < mt*8; i++){
		if (i < len) mr[i] = (text[i] & 0xDF) - 0x30;
		else 	     mr[i] = 0;
	};

	// Generate 7x7 kernel
	// Takes every row, average it and then write to index
	// forward on, substract the previoux, x and y wise

	int   kernel[8][8];
	int   row	 = 0;
	int   rowA	 = 0;
	for(int y = 0; y < 8; y++){
	    for(int x = 0; x < 8; x++){
		for(int n = 0; n < mt; n++){
			if(y & 0x1) 	row += mr[n*8 + (x - y)%8];
			else 		row -= mr[n*8 + (x - y)%8];
		};
		row = (row-x)/(mt+y);
		row = (row) - (rowA);
		rowA = row;
		kernel[y][x] = row;
	    };
	};

	printf("\n");
	// Multiply text matrix with Kernel
	float matrix2[8][8];
	int result = 0;
	for(int y = 0; y < mt; y++){
	    for(int x = 0; x < 8; x++){
		    
		    result = 0;
		    for(int n = 0; n < 8; n++){
				result += (mr[y*8+ n] * kernel[n][x%8])/mt;
		    };
		    matrix2[y%8][x] = result;
	    };
	};
	
	// Create 3x3 subkernel
	printf("\n");
	float ker2[3][3];
	for(int y = 0; y < 3; y++){
	    for(int x = 0; x < 3; x++){
		ker2[y][x] = 0;
		for(int n = 0; n < 8; n++){
		    ker2[y][x] += matrix2[(n+(y*3+x))%8][n];
		};
		ker2[y][x] /= 8;
	    };
	};
	
	for(int m = 0; m < 4; m++)ker2[(8-m)/3][(8-m)%3] = ker2[(7-m)/3][(7-m)%3];
	ker2[1][1] = -1;

	// Apply ker2 to matrix2
	float matrix3[8][8];
	float acc = 0;
	for(int y = 0; y < 8; y++){
	    for(int x = 0; x < 8; x++){
	
		float acc = 0;
		for(int n = 0; n < 3; n++){
	    	    for(int m = 0; m < 3; m++){
			if((y-1+n) < 0)      acc += 0;	
			else if((y-1+n) > 7) acc += 0;			
			else if((x-1+m) < 0) acc += 0;			
			else if((x-1+m) > 7) acc += 0;			
			else                 acc += matrix2[(y-1+n)%8][(x-1+m)%8] * ker2[n][m];			
			};
		    };
		matrix3[y][x] = acc/9;
	    };
	};

	double d = 0;
	for(int n = 0; n < 8; n++){
	    for(int m = 0; m < 8; m++){
	    
		if (n&0x1) d += matrix3[(m+n)%8][m];
		else       d -= matrix3[(m+n)%8][m];

	    };
	};

	d /= (mt*mt);
	d = sin(d*2*M_PI);
	d = 1/(double)(pow(M_E, d) + pow(M_E, -d));
	d = (4*d*d);
	free(mr);
	return d;
}

int main(int argc, char **argv){
	char *input;
	if (argc > 2) 	return 1;
	else 		input = argv[1];

	double a = rate(input, strlen(input));
	printf("%lf\n", a);
	return 0; 
}
