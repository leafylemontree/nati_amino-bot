#include <stdlib.h>
#include <dirent.h>
#include <limits.h>
#include <unistd.h>

char *getpath(){
	char *_PATH_ = (char *)malloc(PATH_MAX * sizeof(char));
	getcwd(_PATH_, PATH_MAX);
	return (char *)_PATH_;
}

int path_up(char *path){
	int a = 0;
	do{
		a++;
	} while (path[a] != '\0' || a > PATH_MAX);

	int b = a;
	do{
		b--;
	} while ((path[b] != '/' && path[b] != '\\') && b >= 0);

	if (b == -1) return -1;
	for(int i = b; i <= a; i++){
		path[i] = '\0';
	};

	if (b == 0) path[0] = '/';
	return 0;
}

int path_cd(char *path, char *folder){

	return 0;
}

void path_close(char *path){
	if (path == NULL) return;
	free(path);
}
