import stateless.generate as G
import stateless.exceptions as E
from stateless.status import *
from stateless.utils import *
import random
random.seed(0)

class MyBytearray:
    def __init__(self, int_arr):
        self.b = bytearray(int_arr)

    def __len__(self):
        return len(self.b)

    def __eq__(self, o):
        if isinstance(o, MyBytearray):
            return self.b == o.b
        return self.b == o

    def __getitem__(self, idx):
        if isinstance(idx, int):
            if len(self.b) <= idx:
                raise E.NeedMoreException()
            return bytes([self.b[idx]])
        elif isinstance(idx, slice):
            if idx.start >= len(self.b):
                raise E.NeedMoreException()
            if idx.stop is not None and idx.stop > len(self.b):
                raise E.NeedMoreException()
            return MyBytearray(self.b[idx])
        else:
            assert False, idx

    def __repr__(self):
        return 'MyBytearray[%s]' % repr(self.b)


class HelloValidate(Validate):
    def __init__(self, exe):
        self.exe = exe

    def validate(self, inputstr_):
        inputstr = MyBytearray(inputstr_)
        try:
            if inputstr[0] != b'H':
                return Status.Incorrect, None
            if inputstr[1] != b'E':
                return Status.Incorrect, None
            if inputstr[2] != b'L':
                return Status.Incorrect, None
            if inputstr[3:5].b != b'LO':
                return Status.Incorrect, None
            return Status.Complete, None
        except E.NeedMoreException as e:
            return Status.Incomplete, None

    def get_cumulative_coverage(self, input_str):
       ...

validator = HelloValidate('')
