struct MATRIX_DATA{
  int    length;
  char   rows;
  char   columns;
  char   enable_read;
  long   open;
  long   close;
  float *data;
};

char c_out[256];

void  structCleanup(struct MATRIX_DATA matrix[], int length){
  for(int i = 0; i < length; i++){
      matrix[i].length    = 0;
      matrix[i].rows      = 0;
      matrix[i].columns   = 0;
      matrix[i].open      = 0;
      matrix[i].close     = 0;
  };
  return;
}

int   getBrackets(char *input, struct MATRIX_DATA matrix[3]){
  long ofs      = 0;                // Text pointer

    for(int i = 0; i < 2; i++){

      // Matrix [i] open

        do{
          ofs++;
        } while (input[ofs] != '(');
        matrix[i].open = ofs;

      // Matrix [i] close

        do{

          if (input[ofs] >= '0' & input[ofs] <= '9' & matrix[i].enable_read == 1) {
            matrix[i].length       += 1;
            matrix[i].enable_read   = 0;

          } else if (input[ofs] == ' '){
            matrix[i].enable_read   = 1;

          } else if (input[ofs] == '\n' & matrix[i].length > 0 & matrix[i].rows == 0) {
              matrix[i].rows        = matrix[i].length;
              matrix[i].enable_read = 1;

          } else if (input[ofs] == '\n'){
            matrix[i].enable_read   = 1;
          };

          ofs++;
        } while (input[ofs] != ')');
        matrix[i].close = ofs;

        matrix[i].columns = (int)(matrix[i].length / matrix[i].rows);
    };

  return 0;
}

int   readMatrixValues(char *input, struct MATRIX_DATA matrix[3]){
  int ofs               = 0;
  int buff_ofs          = 0;
  int data_ofs          = 0;
  char readBuffer[17];

  for(int i = 0; i < 2; i++){

          matrix[i].data            = (float *) malloc(matrix[i].length * sizeof(float));
          matrix[i].enable_read     = 1;
          ofs                       = matrix[i].open;
          buff_ofs                  = 0;
          data_ofs                  = 0;
          for(int j = 0; j < 16; j++) readBuffer[j] = 0;

      while(ofs < matrix[i].close){

         if ((input[ofs] >= '0' & input[ofs] <= '9' | input[ofs] == '.') & buff_ofs < 15) {
             readBuffer[buff_ofs] = input[ofs];
             buff_ofs++;
         };

         if ((buff_ofs != 0) & (input[ofs] == ' ' | input[ofs] == '\n')){
             readBuffer[buff_ofs] = '\0';
             matrix[i].data[data_ofs] = atof(readBuffer);
             data_ofs++;
             buff_ofs = 0;
             for(int j = 0; j < 16; j++) readBuffer[j] = 0;
         };

       ofs++;
     };
    };

  return 0;
}

int   matrix_mul(struct MATRIX_DATA matrix[3]){
  matrix[2].length  = matrix[1].rows * matrix[0].columns;
  matrix[2].rows    = matrix[1].rows;
  matrix[2].columns = matrix[0].columns;
  matrix[2].data    = (float *)malloc(matrix[2].length * sizeof(float));

  int acumulator    = 0;

  for(int i = 0; i < matrix[2].columns; i++){
      for(int j = 0; j < matrix[2].rows; j++){
          acumulator = 0;
          for(int l = 0; l < matrix[2].rows; l++)  acumulator += matrix[0].data[i * matrix[0].rows + l] * matrix[1].data[l * matrix[1].columns + j];
          matrix[2].data[j + i * matrix[2].rows] = acumulator;
      };
  };
  return 0;
}

int   matrix_add(struct MATRIX_DATA matrix[3]){
  for(int i = 0; i < matrix[0].rows; i++){
      for(int j = 0; j < matrix[0].columns; j++){
          matrix[2].data[i + j*matrix[0].rows] = matrix[0].data[i + j*matrix[0].rows] + matrix[1].data[i + j*matrix[0].rows];
      };
  };
  return 0;
}

int   matrix_sub(struct MATRIX_DATA matrix[3]){
  for(int i = 0; i < matrix[0].rows; i++){
      for(int j = 0; j < matrix[0].columns; j++){
          matrix[2].data[i + j*matrix[0].rows] = matrix[0].data[i + j*matrix[0].rows] - matrix[1].data[i + j*matrix[0].rows];
      };
  };
  return 0;
}

void  matrixToString(struct MATRIX_DATA matrix){
  char buffer[17];

  for(int i = 0; i < matrix.length; i++){
    for(int j = 0; j < 17; j++) buffer[j] = 0;
    sprintf(buffer, "%.2f ", matrix.data[i]);
    strcat(c_out, buffer);
    if ((i % matrix.rows) == (matrix.rows - 1)) strcat(c_out, "\n");
  };

  return;
}
