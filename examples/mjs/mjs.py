from stateless.utils import *

class MjsValidate(Validate):
    def __init__(self, exe):
        self.exe = exe

    def _exec(self, exe, fname):
        return do([exe, '-f', fname])

    def _cov(self, res):
        return res.stdout.decode().split('\n')[4]

validator = TinycValidate('./examples/mjs/mjs')

