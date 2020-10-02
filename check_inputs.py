import os.path
import random
from stateless.utils import *
import sys

class PFuzzerValidator(Validate):
    def validate(self, input_str):
        with tempfile.NamedTemporaryFile() as f:
            f.write(input_str)
            f.flush()
            res = self._exec(self.exe, f.name)
            if res.returncode == 0:
                return Status.Complete, None
            print('Invalid value %s' % repr(input_str))
            sys.exit(1)

    def get_cumulative_coverage(self, input_str):
        self.cov_exe = '%s.cov' % self.exe
        self.src_dir, src_ = os.path.split(self.exe)
        self.cov_src = '%s.c' % src_
        with tempfile.NamedTemporaryFile() as f:
            f.write(input_str)
            f.flush()
            res1 = self._exec(self.cov_exe, f.name)
            assert res1.returncode == 0, ('error %s' % str(input_str))
            with chdir(self.src_dir):
                res2 = do(['gcov', '-n', '-b', self.cov_src])
                cov_result = self._cov(res2)
                return cov_result

class PFuzzerMjsValidator(PFuzzerValidator):
    def _exec(self, exe, fname):
        return do([exe, '-f', fname])

    def _cov(self, res):
        s = res.stdout.decode().split('\n')
        assert s[5] == "File 'mjs.c'"
        l = s[6].replace('Lines executed:', '').split(' ')[0][:-1]
        b = s[7].replace('Branches executed:', '').split(' ')[0][:-1]
        return (l, b)

def check_valid_inputs(exe, my_data, name):
    i = 0
    parray = []
    if name == 'mjs':
        pf = PFuzzerMjsValidator(exe)
    else:
        pf = PFuzzerValidator(exe)
    for x in [i.encode() for t,i in my_data]:
        try:
            l, b = pf.get_cumulative_coverage(x)
        except Exception as e:
            print(e)
        #print(l, b, repr(x), file=sys.stderr, flush=True)
        parray.append((l, b))
    return parray


if __name__ == "__main__":
    import importlib.util
    my_module = sys.argv[1]
    name = os.path.basename(my_module).replace('.cov', '')
    my_input = sys.argv[2] # 'pfuzzer/%s.py' % name
    spec = importlib.util.spec_from_file_location("decoder", my_input)
    my_decoder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(my_decoder)
    r = check_valid_inputs(my_module.replace('.cov', ''), my_decoder.inputs, name)
    print(r[-1])
