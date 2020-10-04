lt = len('Time used until input was generated:')
def main(fn):
    data = []
    with open(fn) as f:
        ls = f.readlines()
        while ls:
            l, *ls = ls
            l = l.strip()
            if l.startswith('Time used until input was generated: '):
                t = l[lt:]
            elif len(l) == 0:
                continue
            elif l.startswith("'"):
                data.append((t, l))
            else:
                print(l)
                continue
    print('inputs = [')
    for d in data:
        print('[%s, b%s],' % (d[0], d[1]))
    print(']')

import sys
main(sys.argv[1])
