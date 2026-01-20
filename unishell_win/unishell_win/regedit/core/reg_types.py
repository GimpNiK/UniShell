import winreg
STRING = winreg.REG_SZ
STRINGS = winreg.REG_MULTI_SZ
PATH = winreg.REG_EXPAND_SZ
INTEGER = winreg.REG_DWORD
LONG_INT = winreg.REG_QWORD
BINARY = winreg.REG_BINARY
NONE = winreg.REG_NONE

_REG_TYPE_INT = {
    "STRING": STRING,
    "STRINGS": STRINGS,
    "PATH": PATH,
    "INTEGER": INTEGER, 
    "LONG_INT": LONG_INT, 
    "BINARY": BINARY, 
    "NONE": NONE, 
    
}
_REG_TYPE_STR = {v: k for k, v in _REG_TYPE_INT.items()}


    
def _REG_TYPE_AUTO(value) -> int:
    """Detects registry type based on Python value"""
    if isinstance(value, int):
        if -2147483648 <= value <= 2147483647:
            return INTEGER
        else:
            return LONG_INT
    elif isinstance(value, bytes):
        return BINARY
    elif isinstance(value, list) and all(isinstance(x, str) for x in value):
        return STRINGS
    else:
        value = str(value)
        if "%" in value:
            return PATH
        else:
            return STRING  