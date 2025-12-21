import winreg  
from typing import Iterator, TYPE_CHECKING

if TYPE_CHECKING:
    from .UserType import CurrentUser, User, Users

class AutoRun:
	_regpath = r"Software\Microsoft\Windows\CurrentVersion\Run"
	def __init__(self, user: "CurrentUser|User|Users|str|None" = None) -> None:
		from .UserType import _get_winreg_hkey, _get_winreg_subkey
		
		self.hive = _get_winreg_hkey(user)
		self.key_path = _get_winreg_subkey(user) + "\\" if _get_winreg_subkey(user) else "" + self._regpath
		
	
	def get(self, name: str) -> str:
		"""Получить путь к программе по имени"""
		with winreg.OpenKey(self.hive, self.key_path) as key:
			return winreg.QueryValueEx(key, name)[0]
	
	def set(self, name: str, path: str) -> None:
		"""Установить путь для программы (создать или обновить)"""
		with winreg.OpenKey(self.hive, self.key_path, 0, winreg.KEY_WRITE) as key:
			winreg.SetValueEx(key, name, 0, winreg.REG_SZ, path)
	
	def add(self, name: str, path: str) -> None:
		"""Добавить программу в автозагрузку (alias для set)"""
		self.set(name, path)  # Просто вызывает set
	
	def pop(self, name: str) -> None:
		"""Удалить программу из автозагрузки"""
		with winreg.OpenKey(self.hive, self.key_path, 0, winreg.KEY_WRITE) as key:
			winreg.DeleteValue(key, name)
	
	def all(self) -> dict[str, str]:
		"""Получить все программы в автозагрузке: {имя: путь}"""
		result = {}
		with winreg.OpenKey(self.hive, self.key_path) as key:
			count = winreg.QueryInfoKey(key)[1]
			for i in range(count):
				name, value, _ = winreg.EnumValue(key, i)
				result[name] = value
		return result
	
	def keys(self) -> list[str]:
		"""Получить список имен программ"""
		return list(self.all().keys())
	
	def values(self) -> list[str]:
		"""Получить список путей программ"""
		return list(self.all().values())
	
	def items(self) -> list[tuple[str, str]]:
		"""Получить список пар (имя, путь)"""
		return list(self.all().items())
	
	def __iter__(self) -> Iterator[str]:
		"""Итерация по именам программ"""
		return iter(self.keys())
	
	def __len__(self) -> int:
		"""Количество программ в автозагрузке"""
		return len(self.keys())
	
	def __getitem__(self, key: str|int) -> str:
		if isinstance(key, int):
			# По индексу - возвращаем имя программы
			return self.keys()[key]
		elif isinstance(key, str):
			# По имени - возвращаем путь
			return self.get(key)
		else:
			raise TypeError(f"Invalid key type: {type(key)}")
	
	def __setitem__(self, name: str, path: str) -> None:
		self.set(name, path)
	
	def __delitem__(self, name: str) -> None:
		self.pop(name)
	
	def __contains__(self, name: str) -> bool:
		try:
			self.get(name)
			return True
		except:
			return False
	
	def __repr__(self) -> str:
		return f"<AutoRun: {self.all()}>"