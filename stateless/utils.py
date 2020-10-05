from stateless.status import *
import subprocess
import os
import json

import os
from contextlib import contextmanager
import tempfile

class O:
    def __init__(self, **keys): self.__dict__.update(keys)
    def __repr__(self): return str(self.__dict__)



def do(command, env=None, shell=False, log=False, **args):
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr = subprocess.PIPE,
                              shell=shell,
                              env=dict(os.environ, **({} if env is None else env)))
    stdout, stderr = result.communicate(timeout=10)
    os.makedirs('build', exist_ok=True)
    code = result.returncode
    ecode = ((256-code) * -1) if code > 127 else code
    if log:
        with open('build/do.log', 'a+') as f:
            print(json.dumps({'cmd':command, 'env':env, 'exitcode':ecode, 'ocode':code}), env, file=f)
    return O(cmd=command,returncode=ecode, ocode=result.returncode, stdout=stdout, stderr=stderr)

@contextmanager
def chdir(directory):
    owd = os.getcwd()
    try:
        os.chdir(directory)
        yield directory
    finally:
        os.chdir(owd)


class Validate:

    def __init__(self, exe):
        self.exe = exe

    def validate(self, input_str):
        with tempfile.NamedTemporaryFile() as f:
            f.write(input_str)
            f.flush()
            res = self._exec(self.exe, f.name)
            if res.returncode == 1:
                return Status.Incorrect, None
            elif res.returncode == -1:
                return Status.Incomplete, None
            elif res.returncode == 0:
                return Status.Complete, None
            else:
                assert False, ("Wrong code; %s" % res.returncode)
            
    def _cov(self, res):
        assert res.returncode == 0
        ol = res.stdout.decode().split('\n')
        l = ol[1].replace('Lines executed:', '').split(' ')[0][:-1]
        b = ol[3].replace('Taken at least once:', '').split(' ')[0][:-1]
        return (l,b)
    
    def _exec(self, exe, fname):
        return do([exe, fname])
            
    def get_cumulative_coverage(self, input_str):
        assert input_str is not None
        self.cov_exe = '%s.cov' % self.exe
        self.src_dir, src_ = os.path.split(self.exe)
        self.cov_src = '%s.c' % src_
        with tempfile.NamedTemporaryFile() as f:
            f.write(input_str)
            f.flush()
            res1 = self._exec(self.cov_exe, f.name)
            with chdir(self.src_dir):
                res2 = do(['gcov', '-n', '-b', self.cov_src])
                cov_result = self._cov(res2)
                return cov_result


