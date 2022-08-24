all:
	cc -fPIC -shared -o $^.so *.c
	ls -ltr | grep *.so

target:
	cc -fPIC -shared -o $(name).so $(name).c
	ls -ltr | grep $(name).so

test:
	gcc -o $(name) $(name).c
	./$(name)

clean:
	! rm -r *.so
