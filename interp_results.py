import json
import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()
    for l in lines:
        s = json.loads(l)
        print(bytes(s['output']))

