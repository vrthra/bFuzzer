from stateless.utils import *

class MjsValidate(Validate):
    def __init__(self, exe):
        self.exe = exe

    def _cov(self, res):
        try:
            o = res.stdout.decode().split('\n')
            l = o[6].replace('Lines executed:', '').split(' ')[0][:-1]
            b = o[8].replace('Taken at least once:', '').split(' ')[0][:-1]
            return (l, b)
        except IndexError as e:
            return (-1, -1)

validator = MjsValidate('./examples/mjs/mjs')

