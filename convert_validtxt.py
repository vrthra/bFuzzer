lt = len('Time used until input was generated:')
def main(fn):
    data = []
    with open(fn) as f:
        ls = f.readlines()
        while ls:
            l, *ls = ls
            if l.startswith('Time used until input was generated: '):
                t = l[lt:].strip()
            elif len(l.strip()) == '':
                continue
            elif l.startswith("'"):
                data.append((t, l.strip()))
            else:
                print(l)
                continue
    print('inputs = [')
    for d in data:
        print('[%s, %s],' % (d[0], d[1]))
    print(']')

import sys
main(sys.argv[1])
