from stateless.utils import *

class CjsonValidate(Validate):
    def __init__(self, exe):
        self.exe = exe

validator = CjsonValidate('./examples/cjson/cjson')
