import stateless.generate as G
from stateless.status import *

def validate(inputstr):
    try:
        if inputstr[0] != b'h':
            return Status.Incorrect, None, None
        if len(inputstr) < 3:
            return Status.Incomplete, None, None
        if inputstr[1:3] != b'el':
            return Status.Incorrect, 1, None
        if inputstr[3] != b'l':
            return Status.Incorrect, None, None
        if inputstr[4] != b'o':
            return Status.Incorrect, None, None
        return Status.Complete, None, None
    except G.NeedMoreException as e:
        return Status.Incomplete, None, None

