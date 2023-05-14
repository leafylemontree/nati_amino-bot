int checksum(char *text, int len){
	int accumulator = 0;

	for(int i = 0; i < len; i++){
		accumulator += text[i];
	};
	return accumulator;
}
