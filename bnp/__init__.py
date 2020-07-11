from bnp import mathfunc
from bnp import io
from bnp import conversion
from bnp import scene

__version__ = '0.1.0'


def reload_modules():
    import importlib
    importlib.reload(mathfunc)
    importlib.reload(io)
    importlib.reload(conversion)
    importlib.reload(scene)
    from bnp.conversion import any2np


reload_modules()
