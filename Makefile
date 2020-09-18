run:
	python3 main.py

drun:
	env LC_ALL=C python3 -m pudb main.py


clean:
	find . -name __pycache__ -type d -print0 -prune | xargs -0 -- rm -r

