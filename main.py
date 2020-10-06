import os
import stateless.generate as G
import stateless.exceptions as E
import random
import time
import json
import sys
import string

G.init_set_of_bytes([bytes([i]) for i in range(256)])

def valid_input(validator):
    parray = b''
    while True:
        created_bits = None
        try:
            created_bits = G.generate(validator, parray, 0)
        except E.InputLimitException as e:
            print(str(e))
            G.SEEN_AT.clear()
            continue
        except E.IterationLimitException as e:
            print(str(e))
            G.SEEN_AT.clear()
            continue
        except E.BacktrackLimitException as e:
            print(str(e))
            G.SEEN_AT.clear()
            sys.exit(-1)
        print(repr(created_bits), file=sys.stderr)
        if len(created_bits) < 3 and random.randint(0,10) > 1:
            print('continuing from previous')
            parray = created_bits
            continue
        if random.randrange(len(created_bits)) == 0:
            print('continuing from previous')
            parray = created_bits
            continue
        if created_bits is None:
            continue
        print()
        G.SEEN_AT.clear()
        return created_bits


def run_for(validator, name, secs=None):
    start = time.time()
    if secs is None:
        secs = 10
    lst_generated = []
    with open('examples/results_%s.json' % name, 'a+') as f:
        while (time.time() - start) < secs:
            i = valid_input(validator)
            c = validator.get_cumulative_coverage(i)
            lst_generated.append((i,c, (time.time() - start)))
            print(json.dumps({'output':[j for j in i], 
                              'cumcoverage': c,
                              'time': (time.time() - start)}), 
                  file=f, flush=True)
    return lst_generated

time_to_run = 3600
if __name__ == "__main__":
    import importlib.util
    import sys
    my_module = sys.argv[1]
    name = os.path.basename(my_module)
    spec = importlib.util.spec_from_file_location("decoder", my_module)
    my_decoder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(my_decoder)
    lst = run_for(my_decoder.validator, name, time_to_run)
    for i in lst:
        print(i)
