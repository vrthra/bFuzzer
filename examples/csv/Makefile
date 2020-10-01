csv: csvparser.c
	gcc -g -o csvparser csvparser.c
	gcc -fprofile-arcs -ftest-coverage -g -o csvparser.cov csvparser.c

clean:
	rm -rf *.o csvparser __pycache__/ *.gcda *.gcno build *.cov* *.dSYM
