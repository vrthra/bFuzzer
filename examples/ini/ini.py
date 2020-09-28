import os
import tempfile
import stateless.generate as G
from stateless.status import *

def validate(input_str):
    """ return:
        rv: "complete", "incomplete" or "wrong",
        n: the index of the character -1 if not applicable
        c: the character where error happened  "" if not applicable
    """
    with tempfile.NamedTemporaryFile() as f:
        f.write(input_str.b)
        f.flush()
        cmd = "./examples/ini/ini %s" % f.name

        res = os.system(cmd)
        res = os.WEXITSTATUS(res)
        res = (256-res) * (-1) if res > 127 else res # short conversion
        if res == 1:
            return Status.Incorrect, None, None
        elif res == -1:
            return Status.Incomplete, None, None
        else:
            return Status.Complete, None, None

