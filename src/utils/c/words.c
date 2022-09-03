#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include "dir.h"

char  c_out[32];

const char *main(int length){
  char *path = getpath();

  for(int i = 0; i < 32; i++) c_out[i] = 0;

  strcat(path, "/src/utils/c/text/palabras.txt");


  FILE *input;
  FILE *words = fopen(path, "r");

  path_up(path);

  if(length < 10)  sprintf(path, "%s/0%i.hex", path, length);
  else             sprintf(path, "%s/%i.hex",  path, length);
  fprintf(stdout, "%s\n", path);
  
  input = fopen(path, "r");
  if(input == NULL) return NULL;

  fseek(input, 0l, SEEK_END);
  long file_l = ftell(input) >> 3;

  srand(time(NULL));   // Initialization, should only be called once.
  long offset = (rand() % file_l) << 3;
  long word_ptr = 0;
  fseek(input, offset, SEEK_SET);
  fread(&word_ptr, sizeof(long), 1, input);

  fseek(words, word_ptr, SEEK_SET);
  fread(c_out, sizeof(char), length, words);

  fclose(words);
  fclose(input);
  path_close(path);
  return (char *)c_out;
}
