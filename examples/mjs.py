import os
import subprocess
import tempfile
import stateless.generate as G
from stateless.status import *

def validate(input_str):
    """ return:
        rv: "complete", "incomplete" or "wrong",
        n: the index of the character -1 if not applicable
        c: the character where error happened  "" if not applicable
    """
    try:
        with tempfile.NamedTemporaryFile() as f:
            f.write(input_str.b)
            f.flush()
            cmd = "./examples/mjs/mjs -f %s" % f.name
            p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            stdout,stderr = p.communicate()
            output = stdout
        output = output.decode('utf-8')
        '''
        res = os.system(cmd)
        res = os.WEXITSTATUS(res)
        res = (256-res) * (-1) if res > 127 else res # short conversion
        if res == 1:
            return Status.Incorrect, None, None
        elif res == -1:
            return Status.Incomplete, None, None
        else:
            return Status.Complete, None, None
        '''
        if (output.startswith("MJS error: parse error") and not output.endswith("[]")):
            return Status.Incorrect, None, None
        elif output.startswith("MJS error: parse error") and output.endswith("[]"):
            return Status.Incomplete, None, None
        else:
            return Status.Complete, None, None
    except Exception as e:
        msg = str(e)
        return Status.Incorrect, None, None
