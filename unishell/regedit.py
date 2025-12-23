import platform
if platform.system() == "Windows":
    try:
        from unishell_win import *
    except ImportError:
        raise ImportError("Not found module unishell_win. pip install unishell_win")

else:
    from ._internal.funcs import StubClass
    CurUser = StubClass()
    CurrentUser = StubClass()
    Users = StubClass()
    PATH = StubClass()
    AutoRun = StubClass()
    AutoRunOnce = StubClass()