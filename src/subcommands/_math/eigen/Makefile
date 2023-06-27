all:
	gcc -c poly.c
	gcc -c matrix.c
	gcc -c vector.c
	gcc -c interface.c
	gcc -c image.c
	gcc -c main.c
	gcc -o main main.o matrix.o poly.o vector.o interface.o image.o -lm
	-rm -r *.o
	./main

test:
	gcc -c poly.c
	gcc -c matrix.c
	gcc -c vector.c
	gcc -c interface.c
	gcc -c image.c
	gcc -c main.c
	gcc -g main.o matrix.o poly.o vector.o interface.o image.o -lm
	-rm log.txt
	-rm -r *.o
	valgrind --leak-check=full --log-file=log.txt ./a.out
	vim log.txt

python:
	gcc -c poly.c
	gcc -c matrix.c
	gcc -c vector.c
	gcc -c interface.c
	gcc -c image.c
	gcc -c main.c
	gcc -fPIC -shared -o main.so main.o matrix.o poly.o vector.o interface.o image.o -lm
	-rm -r *.o

