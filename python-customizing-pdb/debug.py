import inspect
import pdb
import sys

from pympler import asizeof


KNOWN_UNITS = {"KB", "MB", "BYTES"}

class Debug(pdb.Pdb):
    def __init__(self, *args, **kwargs):
        super(Debug, self).__init__(*args, **kwargs)
        self.prompt = "[extended-pdb] "

    def format_bytes(self, value: int, unit: str) -> str:
        upper = unit.upper()

        # Forcing BYTES for unknown units
        base_unit = upper if upper in KNOWN_UNITS else "BYTES"

        if base_unit == "KB":
            converted = value / 1000
        elif base_unit == "MB":
            converted = value / 1000000
        else:
            converted = value

        return f"{converted:.2f} {base_unit}"

    def do_args_memory_usage(self, arg: str):
        co = self.curframe.f_code
        dict = self.curframe_locals
        n = co.co_argcount + co.co_kwonlyargcount
        if co.co_flags & inspect.CO_VARARGS: n = n+1
        if co.co_flags & inspect.CO_VARKEYWORDS: n = n+1

        self.message("---- Args memory usage ----")
        for i in range(n):
            name = co.co_varnames[i]
            if name in dict:
                arg_size = asizeof.asizeof(dict[name])
                self.message('%s = %s' % (name, self.format_bytes(arg_size, arg)))
            else:
                self.message('%s = *** undefined ***' % (name,))

    do_amu = do_args_memory_usage


def stop():
    debugger = Debug()
    debugger.set_trace(sys._getframe().f_back)