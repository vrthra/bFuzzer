import sys
import itertools
import random
from stateless.status import *
from stateless.exceptions import *

LOG = False

ITERATION_LIMIT=(256*256 + 10000)
INPUT_LIMIT=1000

SET_OF_BYTES = [bytes([i]) for i in range(256)]
SEEN_AT = []

def init_set_of_bytes(s_bytes):
    global SET_OF_BYTES
    SET_OF_BYTES = s_bytes

def logit(v):
    if LOG:
        print(v, file=sys.stderr)

def new_byte(choices):
    v = random.choice(choices)
    return v

def backtrack(prev_bytes, all_choices, limit=0):
    global SEEN_AT
    if not prev_bytes:
        raise BacktrackLimitException('Cant backtrack beyond zero index')
    if limit == -1:
        raise BacktrackLimitException('Cant backtrack beyond last valid inputs')
    # backtrack one byte
    seen = SEEN_AT[len(prev_bytes)-1]
    SEEN_AT = SEEN_AT[:-1]
    last_byte = prev_bytes[-1]
    logit('backtracking %d %s' % (len(prev_bytes), last_byte))
    #assert (last_byte,) in seen
    prev_bytes = prev_bytes[:-1]
    choices = [i for i in all_choices if i not in seen]
    if not choices:
        return backtrack(prev_bytes, all_choices, limit - 1)
    return seen, prev_bytes, choices

def till_n_length_choices(my_choices, rs):
    return my_choices # disable fudging
    all_choices = []
    for r in range(1, rs+1):
        v = [bytes(b''.join(i)) for i in itertools.product(my_choices, repeat=r)]
        #random.shuffle(v)
        all_choices.extend(v)
    return all_choices

def generate(validator, prev_bytes=None, limit=0):
    global SEEN_AT
    all_choices = SET_OF_BYTES
    if prev_bytes is None: prev_bytes = b''
    seen = set()
    iter_limit = ITERATION_LIMIT
    while iter_limit:
        if len(prev_bytes) > INPUT_LIMIT:
            raise InputLimitException('Exhausted %d bytes' % INPUT_LIMIT)
        iter_limit -= 1
        choices = [i for i in all_choices if i not in seen]
        if not choices:
            seen, prev_bytes, choices = backtrack(prev_bytes, all_choices, limit=-1) # disable

        byte = new_byte(choices)
        cur_bytes = prev_bytes + byte
        l_cur_bytes = len(cur_bytes)

        logit('%s %s' % (cur_bytes, len(cur_bytes)))

        rv, n = validator.validate(cur_bytes)
        if rv == Status.Complete:
            SEEN_AT.append(seen)
            return cur_bytes
        elif rv == Status.Incomplete:
            seen.add(byte)  # dont explore this byte again
            prev_bytes = cur_bytes
            SEEN_AT.append(seen)
            seen = set()

            # reset this if it was modified by incorrect
            all_choices = SET_OF_BYTES
        elif rv == Status.Incorrect:
            if n is None or n == -1:
                seen.add(byte)
                continue
            else:
                #raise Exception('Backtrack disabled..')
                logit("%s %s" % (len(choices), len(seen)))
                if n < len(SEEN_AT):
                    seen = SEEN_AT[n]
                    SEEN_AT = SEEN_AT[:n]
                seen.add(byte)
                rs = len(cur_bytes) - n
                all_choices = till_n_length_choices(SET_OF_BYTES, min(rs, 2))
                prev_bytes = prev_bytes[:n]
        else:
            raise Exception(rv)
    raise IterationLimitException('Exhausted %d loops' % ITERATION_LIMIT)
