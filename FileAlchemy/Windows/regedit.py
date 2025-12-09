import os
import subprocess
import sys
from typing import Dict, List, Optional

try:
	import winreg  # type: ignore
except ImportError as exc:  # pragma: no cover
	raise RuntimeError("Windows-only module: requires winreg and Windows OS") from exc

# pywin32 imports (optional but preferred)
try:  # pragma: no cover - import path
	import win32api  # type: ignore
	import win32security  # type: ignore
	import win32net  # type: ignore
	import win32netcon  # type: ignore
	import ctypes
	_HAS_PYWIN32 = True
except Exception:  # pragma: no cover
	_HAS_PYWIN32 = False

'''
User - пользователь // инициализация пользователя по имени/sid(User(id = ...))
CurUser - текущий пользователь
Users - все пользователи на компьютере

Список атрибутов:
User.id - SID пользователя
User.name - имя пользователя
User.domain - домен пользователя
User.type - тип пользователя

Users.(names / all) - список имен пользователей на компьютере

Список функций:
User(name = "Имя пользователя") - создает объект User
User.create(name = "Имя пользователя", password = "Новый пароль") - создает пользователя ->User
User.password.chg(old = "",new = "") - меняет пароль пользователя
User.delete() - удаляет пользователя

Автозапуск программ:
CurUser
User
Users
     .AutoRun      - автозапуск программы при входе в систему
     .AutoRunOnce  - автозапуск программы один раз
                 .add(name = "Имя программы", path = "Путь к программе") - добавляет программу в автозапуск
                 .remove(name = "Имя программы") - удаляет программу из автозапуска
                 .all - словарь программ в автозапуске (имя - путь)

Добавление в контекстное меню:
CurUser
User
Users
     .ContextMenu - контекстное меню
                 .add(name = "Имя программы", path = "Путь к программе") - добавляет программу в контекстное меню
                 .remove(name = "Имя программы") - удаляет программу из контекстного меню
                 .all - словарь программ в контекстном меню (имя - путь)

Добавление типов файлов(ассоциаций):
CurUser
User
Users
     .FileType  - ассоциации типов файлов
              .add(extension = ".txt", name = "Имя программы", path = "Путь к программе") - добавляет ассоциацию
              .remove(extension = ".txt") - удаляет ассоциацию
              .all - словарь ассоциаций (расширение - программа)
'''
class User:
	_id :str|None = ""

	def __init__(self, id = None, name = None, domain = ""):
		if id and type(self).exists(id): # type: ignore
			self._id = id
		elif name  and type(self).exists(name): # type: ignore
			sid, domain, use = win32security.LookupAccountName(domain, name)
			self._id = win32security.ConvertSidToStringSid(sid)
		else:
			raise ValueError("Пользователь не найден")
	
	@classmethod
	def create(cls, name: str = "", password: str = "", 
               full_name: str = "", description: str = "", 
               flags: int = win32netcon.UF_NORMAL_ACCOUNT | win32netcon.UF_SCRIPT,
               priv: int = win32netcon.USER_PRIV_USER) -> "User":
		"""
		Создает нового пользователя Windows.
		
		Args:
			name: Имя пользователя (обязательно)
			password: Пароль (пустая строка = пароль не требуется)
			full_name: Полное имя пользователя
			description: Описание
			flags: Флаги учетной записи
			priv: Уровень привилегий			
		"""
		user_info = {
			'name': name,
			'password': password,
			'priv': priv,
			'home_dir': None,
			'comment': description,
			'flags': flags,
			'script_path': None
		}
		
		if full_name:
			user_info['full_name'] = full_name
		
		win32net.NetUserAdd(
			"",           # локальный компьютер
			1,              # уровень информации
			user_info
		)
		print(win32net.error)	
		return User(name = name)
	
	def delete(self):
		win32net.NetUserDel(self.domain, self.name) # type: ignore
	
	def password_chg(self, old: str, new: str, domain = "") -> bool:
		netapi32 = ctypes.windll.netapi32
		
		result = netapi32.NetUserChangePassword(
			domain,
			self.name,
			old,
			new
		)
		print(result)
		return result == 0 

	@staticmethod
	def getCurUserSid():
		sid, domain, sid_type = win32security.LookupAccountName(None, win32api.GetUserName())
		id = win32security.ConvertSidToStringSid(sid)
		return id
	@staticmethod
	def exists(id:str|None = None, name = None):
		try:
			if id: 
				sid = win32security.ConvertStringSidToSid(id)
				win32security.LookupAccountSid(None, sid)
			elif name:  
				win32security.LookupAccountName(None, name)
			else:
				return False
			return True
		except win32security.error as e:
			return False
	
	
	#properties
	def get_id(self):
		return self._id
	def set_id(self,value):
		...
	def get_name(self):
		sid = win32security.ConvertStringSidToSid(self._id) # type: ignore
		username, domain, sid_type = win32security.LookupAccountSid(None, sid)
		return username
	def set_name(self,value):
		...
	def get_domain(self) -> str:
		sid = win32security.ConvertStringSidToSid(self._id) # type: ignore
		username, domain, sid_type = win32security.LookupAccountSid(None, sid)
		return domain
	def set_domain(self,value):
		...
	def get_type(self):
		if self._id is None: return None
		sid = win32security.ConvertStringSidToSid(self._id)
		username, domain, sid_type = win32security.LookupAccountSid(None, sid)

		type_names = {
			win32security.SidTypeUser: "User",
			win32security.SidTypeGroup: "Group",
			win32security.SidTypeAlias: "Alias",
			win32security.SidTypeWellKnownGroup: "WellKnownGroup", 
			win32security.SidTypeComputer: "Computer",
			win32security.SidTypeDomain: "Domain"
		}

		return type_names.get(sid_type, None)
	
	def set_type(self,value):
		...
	
	id     = property(get_id,set_id,doc = "SID пользователя") #"SID пользователя"
	name   = property(get_name,set_name)
	domain = property(get_domain,set_domain)
	type   = property(get_type,set_type)
	def __repr__(self):
		return f"User <id = {self.id},name = {self.name}, domain = {self.domain},type = {self.type}"
	

import win32security

def find_user_in_all_domains(username):
    """Ищет пользователя во всех возможных местах"""
    
    locations = [
        (None, "Локальный компьютер"),
        ("", "Локальный компьютер (пустая строка)"),
        (".", "Текущий компьютер"),
        (win32api.GetComputerName(), "По имени компьютера"),
    ]
    
    for domain, description in locations:
        try:
            sid, found_domain, stype = win32security.LookupAccountName(domain, username)
            print(f"✅ Найден в {description}:")
            print(f"   Домен: {found_domain}")
            print(f"   SID: {win32security.ConvertSidToStringSid(sid)}")
            return sid, found_domain
        except win32security.error as e:
            if e.winerror != 1332:  # Не "не найден"
                print(f"❌ Ошибка в {description}: {e}")
    
    print(f"❌ Пользователь '{username}' не найден нигде")
    return None, None

# Проверь где находится Gimp
find_user_in_all_domains("Gimp")
#User(name = "Gimp")
user = User.create(name = "Gimp", password = "123")
print(User(name = "Gimp").password_chg(old = "123", new = "1"))
a = input()