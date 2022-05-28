#include <stdio.h>
#include <time.h>
#include <stdlib.h>

char  c_out[32];

const char *main(int length){
  for(int i = 0; i < 32; i++) c_out[i] = 0;
  FILE *input;
  FILE *words = fopen("/home/leaf_2002/Documents/new-bot/src/text/palabras.txt", "r");

  switch(length){
    case 4 :  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/04.hex", "r"); break;
    case 5 :  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/05.hex", "r"); break;
    case 6 :  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/06.hex", "r"); break;
    case 7 :  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/07.hex", "r"); break;
    case 8 :  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/08.hex", "r"); break;
    case 9 :  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/09.hex", "r"); break;
    case 10:  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/10.hex", "r"); break;
    case 11:  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/11.hex", "r"); break;
    case 12:  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/12.hex", "r"); break;
    case 13:  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/13.hex", "r"); break;
    case 14:  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/14.hex", "r"); break;
    case 15:  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/15.hex", "r"); break;
    case 16:  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/16.hex", "r"); break;
    case 17:  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/17.hex", "r"); break;
    case 18:  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/18.hex", "r"); break;
    case 19:  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/19.hex", "r"); break;
    case 20:  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/20.hex", "r"); break;
    case 21:  input = fopen("/home/leaf_2002/Documents/new-bot/src/text/pp.hex", "r"); break;
    default:  break;
  };

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
  return (char *)c_out;
}
