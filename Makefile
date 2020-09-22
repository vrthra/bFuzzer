V=examples/hellodecoder.py

run:
	env LC_ALL=C python3 main.py $(V)

drun:
	env LC_ALL=C python3 -m pudb main.py $(V)


clean:
	find . -name __pycache__ -type d -print0 -prune | xargs -0 -- rm -r

