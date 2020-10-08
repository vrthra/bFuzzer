mjs: mjs.c
	gcc -g -o mjs mjs.c -ldl 
	gcc -fprofile-arcs -ftest-coverage -g -o mjs.cov mjs.c -ldl 
	#gcc -Wl,--no-as-needed -ldl -fprofile-arcs -ftest-coverage -g -o mjs.cov mjs.c

clean:
	rm -rf *.o mjs __pycache__/ *.gcda *.gcno build *.cov* *.dSYM
