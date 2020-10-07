from stateless.utils import *
import stateless.generate as G

G.LOG = True


class TriValidate(Validate):
    def __init__(self, exe):
        self.exe = exe

validator = TriValidate('./examples/tri/tri')
