run:
	python3 main.py

clean:
	find . -name __pycache__ -type d -print0 -prune | xargs -0 -- rm -r

