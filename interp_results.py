import json
import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()
    for l in lines:
        if l[0] == '#': continue
        s = json.loads(l)
        print(bytes(s['output']))

