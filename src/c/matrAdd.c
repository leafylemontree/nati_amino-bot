#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "matrix.h"


const char *main(char *input){
// const char main(){
  // char input[] = "--matrix -add (\n1 2 3\n4 5 6\n7 8 9\n) (\n1 0 0\n0 1 0\n0 0 1\n)";

  struct MATRIX_DATA matrix[3];     // 0 = Input matrix A
                                    // 1 = Input matrix B
                                    // 2 = Output matrix

  for(int i = 0; i < 256; i++) c_out[i] = 0;
  structCleanup(matrix, 3);
  getBrackets(input, matrix);
  readMatrixValues(input, matrix);
  matrix[2].length  = matrix[0].length;
  matrix[2].rows    = matrix[0].rows;
  matrix[2].data    = (float *)malloc(matrix[2].length * sizeof(float));
  matrix_add(matrix);
  matrixToString(matrix[2]);

  free(matrix[0].data);
  free(matrix[1].data);
  free(matrix[2].data);
  return (char *)c_out;
}
