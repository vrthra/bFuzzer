from stateless.utils import *

class IniValidate(Validate):
    def __init__(self, exe):
        self.exe = exe

validator = IniValidate('./examples/ini/ini')
