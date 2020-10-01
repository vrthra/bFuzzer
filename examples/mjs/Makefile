mjs: mjs.c
	gcc -g -o mjs mjs.c
	gcc -fprofile-arcs -ftest-coverage -g -o mjs.cov mjs.c

clean:
	rm -rf *.o mjs __pycache__/
