from stateless.utils import *

class TinycValidate(Validate):
    def __init__(self, exe):
        self.exe = exe

validator = TinycValidate('./examples/tiny/tiny')
