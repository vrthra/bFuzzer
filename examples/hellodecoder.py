import stateless.generate as G
from stateless.status import *

def validate(inputstr):
    try:
        if inputstr[0] != b'H':
            return Status.Incorrect, None, None
        if inputstr[1] != b'E':
            return Status.Incorrect, None, None
        if inputstr[2] != b'L':
            return Status.Incorrect, None, None
        if inputstr[3:5].b != b'LO':
            return Status.Incorrect, None, None
        return Status.Complete, None, None
    except G.NeedMoreException as e:
        return Status.Incomplete, None, None

