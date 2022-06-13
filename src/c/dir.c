#include <stdio.h>
#include "dir.h"

int main(){
	char *path = getpath();
	printf("%s\n", path);
	
	path_up(path);
	printf("%s\n", path);
	
	path_up(path);
	printf("%s\n", path);
	
	path_up(path);
	printf("%s\n", path);

	path_up(path);
	printf("%s\n", path);
	path_up(path);
	printf("%s\n", path);
	path_up(path);
	printf("%s\n", path);

	path_close(path);
	return 0;
}
