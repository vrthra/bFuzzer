from stateless.utils import *

class MjsValidate(Validate):
    def __init__(self, exe):
        self.exe = exe

    def _exec(self, exe, fname):
        return do([exe, '-f', fname])

    def _cov(self, res):
        l = res.stdout.decode().split('\n')[2].replace('Lines executed:', '').split(' ')[0][:-1]
        b = res.stdout.decode().split('\n')[4].replace('Branches executed:', '').split(' ')[0][:-1]
        return (l, b)

validator = MjsValidate('./examples/mjs/mjs')

