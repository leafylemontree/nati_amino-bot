#include <stdio.h>
#include <stdlib.h>

int main(){
  FILE *words_f = fopen("palabras.txt", "rb");
  fseek(words_f, 0l, SEEK_END);
  long length = ftell(words_f);
  fseek(words_f, 0l, SEEK_SET);
  printf("%li\n", length);
  char *words = (char *)malloc(length * sizeof(char));
  fread(words, length, sizeof(char), words_f);
  fclose(words_f);

  FILE *f_01 = fopen("01.hex", "wb+");
  FILE *f_02 = fopen("02.hex", "wb+");
  FILE *f_03 = fopen("03.hex", "wb+");
  FILE *f_04 = fopen("04.hex", "wb+");
  FILE *f_05 = fopen("05.hex", "wb+");
  FILE *f_06 = fopen("06.hex", "wb+");
  FILE *f_07 = fopen("07.hex", "wb+");
  FILE *f_08 = fopen("08.hex", "wb+");
  FILE *f_09 = fopen("09.hex", "wb+");
  FILE *f_10 = fopen("10.hex", "wb+");
  FILE *f_11 = fopen("11.hex", "wb+");
  FILE *f_12 = fopen("12.hex", "wb+");
  FILE *f_13 = fopen("13.hex", "wb+");
  FILE *f_14 = fopen("14.hex", "wb+");
  FILE *f_15 = fopen("15.hex", "wb+");
  FILE *f_16 = fopen("16.hex", "wb+");
  FILE *f_17 = fopen("17.hex", "wb+");
  FILE *f_18 = fopen("18.hex", "wb+");
  FILE *f_19 = fopen("19.hex", "wb+");
  FILE *f_20 = fopen("20.hex", "wb+");
  FILE *f_pp = fopen("pp.hex", "wb+");

  char buffer[32];
  long o = 0;
  int buf_ofs = 0;
  long last_p = 0;

  while(o < length){

      if(words[o] == '\n'){
          switch(buf_ofs){
            case 1:  fwrite(&last_p, sizeof(long), 1, f_01); break;
            case 2:  fwrite(&last_p, sizeof(long), 1, f_02); break;
            case 3:  fwrite(&last_p, sizeof(long), 1, f_03); break;
            case 4:  fwrite(&last_p, sizeof(long), 1, f_04); break;
            case 5:  fwrite(&last_p, sizeof(long), 1, f_05); break;
            case 6:  fwrite(&last_p, sizeof(long), 1, f_06); break;
            case 7:  fwrite(&last_p, sizeof(long), 1, f_07); break;
            case 8:  fwrite(&last_p, sizeof(long), 1, f_08); break;
            case 9:  fwrite(&last_p, sizeof(long), 1, f_09); break;
            case 10: fwrite(&last_p, sizeof(long), 1, f_10); break;
            case 11: fwrite(&last_p, sizeof(long), 1, f_11); break;
            case 12: fwrite(&last_p, sizeof(long), 1, f_12); break;
            case 13: fwrite(&last_p, sizeof(long), 1, f_13); break;
            case 14: fwrite(&last_p, sizeof(long), 1, f_14); break;
            case 15: fwrite(&last_p, sizeof(long), 1, f_15); break;
            case 16: fwrite(&last_p, sizeof(long), 1, f_16); break;
            case 17: fwrite(&last_p, sizeof(long), 1, f_17); break;
            case 18: fwrite(&last_p, sizeof(long), 1, f_18); break;
            case 19: fwrite(&last_p, sizeof(long), 1, f_19); break;
            case 20: fwrite(&last_p, sizeof(long), 1, f_20); break;
            default: fwrite(&last_p, sizeof(long), 1, f_pp); break;
          };
          for(int i = 0; i < 32; i++) buffer[i] = 0;
          last_p = o+1;
          buf_ofs = 0;
      } else {
        buffer[buf_ofs] = words[o];
        buf_ofs++;
      };

      o++;
  };

  free(words);

  free(f_01);
  free(f_02);
  free(f_03);
  free(f_04);
  free(f_05);
  free(f_06);
  free(f_07);
  free(f_08);
  free(f_09);
  free(f_10);
  free(f_11);
  free(f_12);
  free(f_13);
  free(f_14);
  free(f_15);
  free(f_16);
  free(f_17);
  free(f_18);
  free(f_19);
  free(f_20);
  free(f_pp);

  return 0;
}
