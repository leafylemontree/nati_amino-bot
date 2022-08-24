#include <math.h>
#include <stdio.h>
#include <stdlib.h>

float __add__(int length, float input[]);
float __sub__(int length, float input[]);
float __mul__(int length, float input[]);
float __div__(int length, float input[]);
float __pow__(int length, float input[]);
float __log__(int length, float input[]);
float __sqr__(int length, float input[]);
float __sin__(int length, float input[]);
float __cos__(int length, float input[]);
float __tan__(int length, float input[]);
float __inv__(int length, float input[]);

int   inToFloat(float *input, char *in_text, int length);
int   sumTo(int n);
int   factorial(int n);


int main(int mode, int length, char *in_text){
  float result  = 0;
  float *input  = (float *)malloc(length * sizeof(float));
  inToFloat(input, in_text, length);

  switch(mode){
      case 0  : result = __add__(length, input);
                break;
      case 1  : result = __sub__(length, input);
                break;
      case 2  : result = __mul__(length, input);
                break;
      case 3  : result = __div__(length, input);
                break;
      case 4  : result = __pow__(length, input);
                break;
      case 5  : result = __log__(length, input);
                break;
      case 6  : result = __sqr__(length, input);
                break;
      case 7  : result = __sin__(length, input);
                break;
      case 8  : result = __cos__(length, input);
                break;
      case 9  : result = __tan__(length, input);
                break;
      case 10 : result = __inv__(length, input);
                break;
  };

  free(input);
  return result;
}

float __add__(int length, float input[]){
  float result = 0;
  for(int i = 0; i < length; i++)   result += input[i];
  return (float)result;
}

float __sub__(int length, float input[]){
  float result = input[0];
  for(int i = 1; i < length; i++)   result -= input[i];
  return (float)result;
}

float __mul__(int length, float input[]){
  float result = 1;
  for(int i = 0; i < length; i++)   result = result * input[i];
  return (float)result;
}

float __div__(int length, float input[]){
  float result = input[0];
  if (input[1] == 0) return 0;

  for(int i = 1; i < length; i++)   result = result / input[i];
  return (float)result;
}

float __pow__(int length, float input[]){
  float result = 0;
  result = pow(input[0], input[1]);
  return (float)result;
}

float __log__(int length, float input[]){
  float result = 0;
  if (length == 1) result = log(input[0]);
  else result = log(input[0]) / log(input[1]);
  return (float)result;
}

float __sqr__(int length, float input[]){
  float result = 0;
  if (input[0] < 0) return 0;

  result = sqrt(input[0]);
  return (float)result;
}

float __sin__(int length, float input[]){
  float  result     = 0;
  double acumulator = 0;

  float  x          = input[0];
  float  xn         = x;
  int    iterations = 16;

  // sumTo = (n * (n+1))/2;

  for(int i = 1; i <= iterations; i++){
      acumulator = xn / factorial(2*i - 1);
      if (!(i & 0x1)) acumulator = acumulator * -1;
      result += acumulator;
      xn = xn * x * x;
  };

  return (float)result;
}

float __cos__(int length, float input[]){
  float result = 0;
  return (float)result;
}

float __tan__(int length, float input[]){
  float result = 0;
  return (float)result;
}

float __inv__(int length, float input[]){
  float result = 0;
  result = 1/input[0];
  return (float)result;
}

int   inToFloat(float input[], char *in_text, int length){
  unsigned char readBuffer[25];
  int           ofs             = 0;
  int           buff_o          = 0;

  for(int i = 0; i < length; i++){

      buff_o = 0;
      for(int j = 0; j < 25; j++)     readBuffer[j] = 0;

      while (in_text[ofs] != '_'){

        if (in_text[ofs] >= '0' & in_text[ofs] <= '9' | in_text[ofs] == '.' | in_text[ofs] == '-'){
            readBuffer[buff_o] = in_text[ofs];
            buff_o++;
        };

        ofs++;
      };

      readBuffer[buff_o] = '\0';
      input[i] = atof(readBuffer);
      ofs++;
  };
  return 0;
}

int sumTo(int n){
  return ((n*(n + 1))/2);
}

int factorial(int n){
  int result = 1;
  for(int i = 2; i <= n; i++) result = result * i;
  return result;
}
