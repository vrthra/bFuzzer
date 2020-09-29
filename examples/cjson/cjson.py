import os
import subprocess
import tempfile
import stateless.generate as G
from stateless.status import *

def validate(input_str):
    with tempfile.NamedTemporaryFile() as f:
        f.write(input_str.b)
        f.flush()
        cmd = "./examples/cjson/cjson -f %s" % f.name
        res = os.system(cmd)
        res = os.WEXITSTATUS(res)
        res = (256-res) * (-1) if res > 127 else res # short conversion
        if res == 1:
            return Status.Incorrect, None, None
        elif res == -1:
            return Status.Incomplete, None, None
        else:
            return Status.Complete, None, None
