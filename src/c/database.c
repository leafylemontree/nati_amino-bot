#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "dir.h"


struct __USER__ {
  int   version;
  char  alias[128];
  int   hugs[2];
  int   kiss[2];
  int   pats[2];
  int   doxx[2];
  int   kiwi;
  int	derr;
  int	win;
  int 	draw;
  int 	points;
  int   plac[12];
  char fileEnd;
} user;

char *_dir_c;
char c_out[512];

int createUser(char *uid);
int getUserInfo(char *uid);
int writeData(char *uid);
void initStruct();


const char *main(int mode, char *uid, char *extra)
{
  _dir_c = getpath();
  strcat(_dir_c, "/database/");
  fprintf(stdout, "%s\n", _dir_c);

  for(int i = 0; i < 512; i++) c_out[i] = 0;
  initStruct();
  switch(mode){
    case  0: // Create user
              createUser(uid);
              break;
    case 1:  // Retrieve user
              getUserInfo(uid);
              sprintf(c_out, "%s__$%i__$%i__$%i__$%i__$%i__$%i__$%i__$%i__$%i__$%i__$%i__$%i__$%i",
			      user.alias,
			      user.hugs[0],
			      user.hugs[1],
			      user.kiss[0],
			      user.kiss[1],
			      user.pats[0],
			      user.pats[1],
			      user.doxx[0],
			      user.doxx[1],
			      user.kiwi,
			      user.derr,
			      user.win,
			      user.draw,
			      user.points
			      );
              break;

    case 10:  // Init r_all
              getUserInfo(uid);
              user.hugs[0] = 0;
              user.kiss[0] = 0;
              user.pats[0] = 0;
              writeData(uid);
              // strcat(c_out, "%i", 200);
              break;

    case 11:  // Add 1 received hug
              getUserInfo(uid);
              user.hugs[0]++;
              writeData(uid);
              // strcat(c_out, "%i", 200);
              break;

    case 12:  // Add 1 received kiss
              getUserInfo(uid);
              user.kiss[0]++;
              writeData(uid);
              // strcat(c_out, "%i", 200);
              break;

    case 13:  // Add 1 received pat
              getUserInfo(uid);
              user.pats[0]++;
              writeData(uid);
              // strcat(c_out, "%i", 200);
              break;

    case 14:  // Add 1 received pat
              getUserInfo(uid);
              user.doxx[1]++;
              writeData(uid);
              // strcat(c_out, "%i", 200);
              break;

    case 20:  // Init g_all
              getUserInfo(uid);
              user.hugs[1] = 0;
              user.kiss[1] = 0;
              user.pats[1] = 0;
              writeData(uid);
              // strcat(c_out, "%i", 200);
              break;

    case 21:  // Add 1 gived hug
              getUserInfo(uid);
              user.hugs[1]++;
              writeData(uid);
              // strcat(c_out, "%i", 200);
              break;

    case 22:  // Add 1 gived kiss
              getUserInfo(uid);
              user.kiss[0]++;
              writeData(uid);
              // strcat(c_out, "%i", 200);
              break;

    case 23:  // Add 1 gived pat
              getUserInfo(uid);
              user.pats[1]++;
              writeData(uid);
              // strcat(c_out, "%i", 200);
              break;

    case 24:  // Add 1 received pat
              getUserInfo(uid);
              user.doxx[1]++;
              writeData(uid);
              // strcat(c_out, "%i", 200);
              break;

    // case 30: // return Alias
    case 31: // Change Alias
              getUserInfo(uid);
              for(int i = 0; i < 128; i++) user.alias[i] = 0;
              strcat(user.alias, extra);
              writeData(uid);
              // strcat(c_out, "%i", 200);
              break;

    case 32:  // Add 1 received pat
              getUserInfo(uid);
              user.kiwi++;
              writeData(uid);
              // strcat(c_out, "%i", 200);
              break;

    case 41: // Add 1 defeat
	      getUserInfo(uid);
	      user.derr++;
	      writeData(uid);
	      break;
 
 
    case 42: // Add 1 win
	      getUserInfo(uid);
	      user.win++;
	      writeData(uid);
	      break;
 
    case 43: // Add 1 draw
	      getUserInfo(uid);
	      user.draw++;
	      writeData(uid);
	      break;
 
    case 44: // Add x points
	      getUserInfo(uid);
	      user.points += atoi(extra);
	      writeData(uid);
	      break;
 
  };

  path_close(_dir_c);
  return c_out;
}

int createUser(char *uid){
    char buffer[128];
    for(int i = 0; i < 128; i++) buffer[i] = 0;
    strcat(buffer, _dir_c);
    strcat(buffer, uid);
    strcat(buffer, ".hex");
    printf("%s\n", buffer);

    FILE *data = fopen(buffer, "r");
    if (data != NULL){
      printf("File exists\n");
      fclose(data);
      return 1;
    };

    data = fopen(buffer, "wb+");
    initStruct();
    printf("%li\n", sizeof(struct __USER__));
    fwrite(&user, sizeof(struct __USER__), 1, data);
    fclose(data);
    return 0;
}

int getUserInfo(char *uid){
  char buffer[128];
  for(int i = 0; i < 128; i++) buffer[i] = 0;
  strcat(buffer, _dir_c);
  strcat(buffer, uid);
  strcat(buffer, ".hex");

  FILE *data = fopen(buffer, "rb+");
  if (data == NULL){
    initStruct();
    return -1;
  } else {
    fread(&user, sizeof(struct __USER__), 1, data);
    fclose(data);
  };
  return 0;
}

int writeData(char *uid){
  char buffer[128];
  for(int i = 0; i < 128; i++) buffer[i] = 0;
  strcat(buffer, _dir_c);
  strcat(buffer, uid);
  strcat(buffer, ".hex");
  fprintf(stdout, "%s\n", buffer);

  FILE *data_w = fopen(buffer, "wb+");
  if (data_w == NULL){
    fprintf(stdout, "Error al abrir\n");
    return 1;
  };
  fwrite(&user, sizeof(struct __USER__), 1, data_w);
  fclose(data_w);
  return 0;
}

void initStruct(){
  user.version = 2;
  for(int i = 0; i < 128; i++) user.alias[i] = 0;
  user.hugs[0] = 0;
  user.kiss[0] = 0;
  user.pats[0] = 0;
  user.doxx[0] = 0;
  user.hugs[1] = 0;
  user.kiss[1] = 0;
  user.pats[1] = 0;
  user.doxx[1] = 0;
  user.derr    = 0;
  user.win     = 0;
  user.draw    = 0;
  user.points  = 0;
  for(int i = 0; i < 12; i++) user.plac[i] = 0;
  user.fileEnd = 0xFF;
  return;
}
