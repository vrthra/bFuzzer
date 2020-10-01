from stateless.utils import *

class CsvValidate(Validate):
    def __init__(self, exe):
        self.exe = exe

validator = CsvValidate('./examples/csv/csvparser')
