#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <unistd.h>
#include <limits.h>
#include <string.h>

struct __USER_1__ {
  char  alias[32];
  int   hugs[2];
  int   kiss[2];
  int   pats[2];

  char fileEnd;
} user_old;

struct __USER_2__ {
  int   version;
  char  alias[128];
  int   hugs[2];
  int   kiss[2];
  int   pats[2];
  int   doxx[2];
  int   kiwi;

  int   plac[16];
  char fileEnd;
} user_new;

void translationUnit();

int main(){
  DIR *d;
  struct dirent *dir;
  FILE *fptr;
  char cwd[PATH_MAX];

  getcwd(cwd, sizeof(cwd));
  strcat(cwd, "/database_out");
  printf("dir: %s\n", cwd);

  d = opendir(cwd);

  if(d == NULL)  return -1;

  char fpath[4096];

   while((dir = readdir(d)) != NULL){


      if(!(dir->d_name[0] == '.' || dir->d_name[1] == '.')){

              printf("file: %s\n", dir->d_name);

              for(int i = 0; i < 4096; i++) fpath[i] = 0;
              strcat(fpath, cwd);
              strcat(fpath, "/");
              strcat(fpath, dir->d_name);


              fptr = fopen(fpath, "rb+");
              if(fptr == NULL) {
                  printf("error: file1\n");
                  return -1;
                };

              fread(&user_old, sizeof(struct __USER_1__), 1, fptr);
              translationUnit();
              fseek(fptr, 0l, SEEK_SET);
              fwrite(&user_new, sizeof(struct __USER_2__), 1, fptr);
              fclose(fptr);
            };

      };


  closedir(d);

  return 0;
}

void translationUnit(){
  user_new.version = 2;

  for(int i = 0; i < 128; i++) user_new.alias[i] = 0;
  strcat(user_new.alias, user_old.alias);

  for(int i = 0; i < 2; i++){
    user_new.hugs[i] = user_old.hugs[i];
    user_new.kiss[i] = user_old.kiss[i];
    user_new.pats[i] = user_old.pats[i];
    user_new.doxx[i] = 0;
  };

  user_new.kiwi = 0;
  for(int i = 0; i < 16; i++) user_new.plac[i] = 0;

  return;
}
