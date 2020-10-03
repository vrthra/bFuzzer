mjs: mjs.c
	gcc -ldl -g -o mjs mjs.c
	gcc -ldl -fprofile-arcs -ftest-coverage -g -o mjs.cov mjs.c

clean:
	rm -rf *.o mjs __pycache__/ *.gcda *.gcno build *.cov* *.dSYM
