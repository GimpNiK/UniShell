# project_root = r"C:\Users\ПК\Desktop\UniShell\unishell"
# import sys
# sys.path.insert(0, project_root)
# project_root = r"C:\Users\ПК\Desktop\UniShell\unishell_win"
# sys.path.insert(0, project_root)

from unishell.regedit import *
import winreg
registry = Registry("HKCU")
registry2 = Registry(winreg.HKEY_CURRENT_USER) 

user_sid = CurUser.id
registry3 = Registry(user_sid) # Получение куста(раздела реестра) по SID пользователя
registry4 = Registry(CurUser)

#Вывод ключей реестра находящихся в главном кусте
print(registry.containers()) #['AppEvents', 'Console', ...]

#Создаем конфиги приложения для текущего пользователя
myapp = registry / "Software" / "MyApp"
myapp["version"] = "1.2.3"                                 #STRING
myapp["dependies"] = ["winreg","unishell"]                 #STRINGS
myapp["num_load"] = 0                                      #INTEGER
myapp["int64"] = 2**32 + 5                                 #LONG_INT
myapp["all_users"] = False                                 #INTEGER
myapp["dir_for_install"] = "%USERPROFILE%\\AppData\\MyApp" #PATH
myapp["bin"] = bytes([1,1,1])

print(myapp.json(use_types = True))
#{'version': ('1.2.3', 'STRING'), 'dependies': (['winreg', 'unishell'], 'STRINGS'), 'num_load': (0, 'INTEGER'), 'int64': (4294967301, 'LONG_INT'), 'all_users': (0, 'INTEGER'), 'dir_for_install': ('%USERPROFILE%\\AppData\\MyApp', 'PATH'), 'bin': (b'\x01\x01\x01', 'BINARY')}
from unishell_win.regedit.core.Registry import *
Field(myapp,"dir_for_install").set("%USERPROFILE%\\AppData\\MyApp",STRING) 

from unishell import File
import json
import base64

class BytesEncoder(json.JSONEncoder):   
    def default(self, obj):
        if isinstance(obj, bytes):
            return {
                '__type__': 'bytes',
                'value': base64.b64encode(obj).decode('utf-8')
            }
        return super().default(obj)

def bytes_decoder(dct):
    if '__type__' in dct and dct['__type__'] == 'bytes':
        return base64.b64decode(dct['value'].encode('utf-8'))
    return dct

HKCU_backup = json.dumps(registry.json(use_types=True),cls=BytesEncoder)
File("HKCU_backup.json")< HKCU_backup

HKCU_backup = File("HKCU_backup.json").content
HKCU_json = json.loads(HKCU_backup, object_hook=bytes_decoder)
registry.from_json(HKCU_json,use_types=True) #Требуются права админа
#.reg - 100 Мб vs json(use_types=True) - 24 Мб vs json(use_types=False) - 23 Мб