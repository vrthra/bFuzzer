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
            cmd = "./examples/tiny/tiny %s" % f.name
            p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            stdout,stderr = p.communicate()
            output = stderr
            output = output.decode("utf-8")
        if output.startswith("syntax"):
            return Status.Incorrect, None, None
        elif output.startswith("EOF"):
            return Status.Incomplete, None, None
        elif output.find("Syntax error") != -1:
            return Status.Incorrect, None, None
        else:
            return Status.Complete, None, None
    except Exception as e:
        msg = str(e)
        if msg.endswith("exit status 1"):
            pass
        else:
            pass
        n = len(msg)
        return Status.Incorrect, None, None

