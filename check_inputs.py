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
        b = s[8].replace('Taken at least once:', '').split(' ')[0][:-1]
        return (l, b)

def check_valid_inputs(exe, my_data, name):
    lst_generated = []
    pf = (PFuzzerMjsValidator(exe) if name == 'mjs' else PFuzzerValidator(exe))

    with open('examples/results_%s.json' % name, 'w+') as f:
        for i,(t,b) in enumerate(my_data):
            try:
                c = pf.get_cumulative_coverage(b)
                lst_generated.append((i,c))
                print(json.dumps({'output':[j for j in b], 
                                  'cumcoverage': c,
                                  'time': t}), 
                      file=f, flush=True)
            except Exception as e:
                print(i, e)
    return lst_generated


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
