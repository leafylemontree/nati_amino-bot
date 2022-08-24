#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

char buffer_out[512];

struct __VARIABLE__ {
      char *label;
      int   loc;
      double value;
};

struct __GLOBAL__ {
    int vars;
    int lines;
    char c_out[2000];
} __global__;


struct __VARIABLE__ *getVars(char *input);
int removeWhitespace(char *input);
int searchVar(struct __VARIABLE__ *var, char *buffer);
int readNextValue(int *ofs, char *buffer, char *input);
int getLines(char *input);
int readOP(char *input, int *of);
int applyFunc(int op, struct __VARIABLE__ *var, int *of_, char *input);

const char *main(char *input){
// const char *main(){
  printf("%s\n\n", input);
  removeWhitespace(input);
  printf("%s\n\n", input);

  for(int i = 0; i < 256; i++) __global__.c_out[i] = 0;

  int  op      = -1;
  int  of      =  0;

  struct __VARIABLE__ *var = getVars(input);
  __global__.lines = getLines(input);

  for(int i = 0; i < (__global__.lines - __global__.vars); i++){
    op = readOP(input, &of);
    applyFunc(op, var, &of, input);
  };

  fprintf(stdout, "%s\n", __global__.c_out);
  free(var);

  return (char *)__global__.c_out;
}


int readNextValue(int *ofs_, char *buffer, char *input){
  for(int i = 0; i < 16; i++) buffer[i] = 0;

  int buff_ofs  = 0;
  int ret_val   = 0;
  int ofs       = *ofs_;

  while(input[ofs] == ' ' || input[ofs] == '\n'){
     ofs++;
   };
  do{
      if (buff_ofs < 16){
        buffer[buff_ofs] = input[ofs];
      } else ret_val = 1;

      buff_ofs++;
      ofs += 1;
  } while (input[ofs] != ' ' && input[ofs] != '\n' && input[ofs] != '\0');

  if (buff_ofs < 16) buffer[buff_ofs] = '\0';
  *ofs_ = ofs;
  return 0;
}

struct __VARIABLE__ *getVars(char *input){
  int  n   = 0;
  int  ofs = 0;
  char buffer1[16];
  char buffer2[16];

  while(1){
    readNextValue(&ofs, buffer1, input);
    if(!strcmp(buffer1, "VAR")){
      n++;
      readNextValue(&ofs, buffer1, input);
      readNextValue(&ofs, buffer2, input);
    };
    if (buffer1[0] == '}') break;
  };

  ofs = 0;
  struct __VARIABLE__ *var = (struct __VARIABLE__ *) malloc(n * sizeof(struct __VARIABLE__));

  n   = 0;
  while(1){
    readNextValue(&ofs, buffer1, input);
    if(!strcmp(buffer1, "VAR")){
      readNextValue(&ofs, buffer1, input);
      readNextValue(&ofs, buffer2, input);

      var[n].label                                                = (char *)malloc(  strlen(buffer1) * sizeof(char) +1 );
      for(int i = 0; i < strlen(buffer1) +1; i++) var[n].label[i] = buffer1[i];
      var[n].value                                                = atof(buffer2);
      n++;
    };

    if (buffer1[0] == '}') break;
  };

  __global__.vars = n;
  return var;
}

int searchVar(struct __VARIABLE__ *var, char *buffer){
  for(int i = 0; i < __global__.vars; i++){
      if(!strcmp(var[i].label, buffer))      return i;
  };
  return -1;
}

int getLines(char *input){
  int lines = 0;
  for(int i = 0; i < strlen(input); i++){
    if(input[i] == '\n' || input[i] == '\0') lines++;
  };
  return lines - 1;
}

int readOP(char *input, int *of_){
  int  op  = -1;
  char buffer[16];
  int  of = *of_;

  while(1){
    readNextValue(&of, buffer, input);
    if      (!strcmp(buffer, "ADD"))   op =  0;
    else if (!strcmp(buffer, "SUB"))   op =  1;
    else if (!strcmp(buffer, "MUL"))   op =  2;
    else if (!strcmp(buffer, "DIV"))   op =  3;
    else if (!strcmp(buffer, "POW"))   op =  4;
    else if (!strcmp(buffer, "SQR"))   op =  5;
    else if (!strcmp(buffer, "LOG"))   op =  6;
    else if (!strcmp(buffer, "PRINT")) op =  7;
    else                               op = -1;

    if(op != -1) break;
  };
  *of_ = of;
  return op;
}

int applyFunc(int op, struct __VARIABLE__ *var, int *of_, char *input){
  char   buffer1[16];
  char   buffer2[16];
  int    of           = *of_;
  int    n1     = 0;
  int    n2     = 0;
  double  memory = 0;
  double  m      = 0;
  int    op_cnt = 0;

  char   buf_out[256];

  readNextValue(&of, buffer1, input);
  n1 = searchVar(var, buffer1);
  if(n1 == -1) return -1;
  memory = var[n1].value;

  if(op == 7) {
    for(int i = 0; i < 32; i++) buf_out[i] = 0;
    sprintf(buf_out, "%s = %lf\n", var[n1].label, var[n1].value);
    strcat(__global__.c_out, buf_out);
    *of_ = of;
    return 0;
  } else if (op == 5){

    memory = sqrt(memory);
    var[n1].value = memory;
    while (input[of] != '\n') of++;
    if(input[of] == '\n'){
      *of_ = of;
      return -1;
    };
  };

  while(input[of] != '\n' && input[of] != '\0'){

    while (input[of] == ' ') of++;

    if(input[of-1] == '\n') return -1;

      readNextValue(&of, buffer2, input);
      n2 = searchVar(var, buffer2);

      if(buffer2[0] == '}') return -1;

      if (n2 == -1) m = atof(buffer2);
      else          m = var[n2].value;


      fprintf(stdout, "CHECK: %i %f %f", op, memory, m);
      switch(op){
          case   0  : memory = memory + m;
                      break;
          case   1  : memory = memory - m;
                      break;
          case   2  : memory = memory * m;
                      break;
          case   3  : memory = memory / m;
                      break;
          case   4  : memory = pow(memory, m);
                      break;
          case   6  : memory = log(memory)/ log(m);
                      break;
        };

    var[n1].value = memory;

    of++;
    op_cnt++;
  };

  *of_ = of;
  return 0;
}

int removeWhitespace(char *input){
  int read  = 1;
  int ofs1  = 0;    // input
  int ofs2  = 0;    // buffer
  long len = strlen(input);
  fprintf(stdout, "%li\n", len);

  char *buffer = (char *)malloc(len * sizeof(char));
  for(int i = 0; i < len; i++) buffer[i] = input[i];

  for(int i = 0; i < len; i++){
    ofs2 = i;

    if(buffer[i] == '#') read = 2;
    if(buffer[i] == '\0') break;

    if(read == 0){
      if(buffer[i] != ' ' && buffer[i] != '\n')  read = 1;
      if(buffer[i] == '\0') break;
    };

    if (read == 1){
      input[ofs1] = buffer[i];
      ofs1++;
    };

    if(buffer[i] == '\n') read = 0;

    if(read == 2){
      if(buffer[i] == '\n')  read = 1;
      if(buffer[i] == '\0') break;
    };

  };

  for(int i = ofs1; i < ofs2; i++) input[i]=0;

  free(buffer);
  return 0;
}
