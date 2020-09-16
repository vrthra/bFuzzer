import sys
import random
import enum

class Status(enum.Enum):
    Complete = 0
    Incomplete = 1
    Incorrect = -1

SET_OF_BYTES = [i for i in range(256)]
SEEN_AT = []

def logit(v):
    print(v, file=sys.stderr)

def new_byte(choices): return random.choice(choices)

def generate(validate, prev_bytes=None):
    global SEEN_AT
    if prev_bytes is None: prev_bytes = []
    seen = set()
    while True:
        choices = [i for i in SET_OF_BYTES if i not in seen]
        if not choices:
            # backtrack one byte
            seen = SEEN_AT[len(prev_bytes)]
            last_byte = prev_bytes[-1]
            logit('backtracking', len(prev_bytes), last_byte)
            seen.add(last_byte) # dont explore this byte again
            prev_bytes = prev_bytes[:-1]
            choices = [i for i in SET_OF_BYTES if i not in seen]

        byte = new_byte(choices)
        cur_bytes = prev_bytes + [byte]
        l_cur_bytes = len(cur_bytes)

        if l_cur_bytes >= len(SEEN_AT):
            SEEN_AT.append(set())
        SEEN_AT[len(cur_bytes)-1].add(byte) 

        ib = MyBytearray(cur_bytes)
        logit('%s..%s, %s' % (ib.ba[0:20], ib.ba[-10:], len(ib.ba)))
        rv, _n, _at = validate(ib)
        if rv == Status.Complete:
            return ib
        elif rv == Status.Incomplete:
            seen.clear()
            prev_bytes = cur_bytes
            if len(prev_bytes) < len(SEEN_AT):
                SEEN_AT = SEEN_AT[:-1]
        elif rv == Status.Incorrect:
            seen.add(byte)
        else:
            raise Exception(rv)
    return None

class NeedMoreException(Exception): ...

class MyBytearray:
    def __init__(self, int_arr):
        self.ba = bytearray(int_arr)

    def __len__(self):
        return len(self.ba)

    def __getitem__(self, idx):
        if isinstance(idx, int):
            if len(self.ba) <= idx:
                raise NeedMoreException()
            return self.ba[idx]
        elif isinstance(idx, slice):
            if idx.start >= len(self.ba):
                raise NeedMoreException()
            if idx.stop is not None and idx.stop >= len(self.ba):
                raise NeedMoreException()
            return MyBytearray(self.ba[idx])
        else:
            assert False, idx

