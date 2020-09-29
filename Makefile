SRC=examples/cjson/ examples/csv/ examples/ini/ examples/mjs/ examples/tiny/
V=examples/hellodecoder.py

run:
	env LC_ALL=C python3 main.py $(V)

drun:
	env LC_ALL=C python3 -m pudb main.py $(V)


clean:
	find . -name __pycache__ -type d -print0 -prune | xargs -0 -- rm -r
	for i in $(SRC); do (cd $$i; make clean); done

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



