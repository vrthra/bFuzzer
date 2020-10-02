SRC=examples/cjson/ examples/csv/ examples/ini/ examples/mjs/ examples/tiny/
V=examples/hellodecoder.py

run:
	env LC_ALL=C python3 main.py $(V)

drun:
	env LC_ALL=C python3 -m pudb main.py $(V)


clean:
	find . -name __pycache__ -type d -print0 -prune | xargs -0 -- rm -r
	for i in $(SRC); do (cd $$i; make clean); done
	rm -rf examples/results_*.json

compile:
	for i in $(SRC); do (cd $$i; make); done

cjson:
	make run V=examples/cjson/cjson.py

csv:
	make run V=examples/csv/csvparser.py

ini:
	make run V=examples/ini/ini.py

tiny:
	make run V=examples/tiny/tinyc.py

mjs:
	make run V=examples/mjs/mjs.py

all_bfuzzer: tiny cjson mjs ini csv
	@echo done

pFuzz:
	$(MAKE) clean
	$(MAKE) compile
	env LC_ALL=C python3 check_inputs.py examples/cjson/cjson.cov pfuzzer/cjson.py
	env LC_ALL=C python3 check_inputs.py examples/csv/csvparser.cov pfuzzer/csvparser.py
	env LC_ALL=C python3 check_inputs.py examples/ini/ini.cov pfuzzer/ini.py
	env LC_ALL=C python3 check_inputs.py examples/mjs/mjs.cov pfuzzer/mjs.py
	env LC_ALL=C python3 check_inputs.py examples/tiny/tiny.cov pfuzzer/tiny.py
	mv examples/results_* pfuzzer/


simple:
	$(MAKE) clean
	$(MAKE) compile
	env LC_ALL=C python3 check_inputs.py examples/cjson/cjson.cov simplechains/cjson.py
	env LC_ALL=C python3 check_inputs.py examples/csv/csvparser.cov simplechains/csvparser.py
	env LC_ALL=C python3 check_inputs.py examples/ini/ini.cov simplechains/ini.py
	env LC_ALL=C python3 check_inputs.py examples/mjs/mjs.cov simplechains/mjs.py
	env LC_ALL=C python3 check_inputs.py examples/tiny/tiny.cov simplechains/tiny.py
	mv examples/results_* simplechains/


