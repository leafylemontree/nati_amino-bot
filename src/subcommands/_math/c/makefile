all:
	cc -fPIC -shared -o $^.so *.c
	ls -ltr | grep *.so

target:
	cc -fPIC -shared -o $(name).so $(name).c -lm
	ls -ltr | grep $(name).so

test:
	gcc -o $(name) $(name).c -lm
	./$(name)

clean:
	! rm -r *.so
