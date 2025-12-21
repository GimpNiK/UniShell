import winreg  
from typing import Iterator, TYPE_CHECKING

if TYPE_CHECKING:
    from .UserType import CurrentUser, User, Users
class PATH:
	_regpath = r"Environment"
	"""
	user: CurrentUser | User | Users | User_id:str | None
	PATH(user).add(path)
			   .pop(path)
			   .all()
	for path in PATH(user):
		pass
	for i in range(len(PATH(user))):
		PATH(user[i])
	"""

	def __init__(self, user: "CurrentUser|User|Users|str|None" = None) -> None:
		from .UserType import Users, _get_winreg_hkey, _get_winreg_subkey
		

		self.hive = _get_winreg_hkey(user)
		self.key_path = _get_winreg_subkey(user) + "\\" if _get_winreg_subkey(user) else "" + self._regpath
		
		if isinstance(user, Users):
			self.hive = winreg.HKEY_LOCAL_MACHINE
			self.key_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"


	def get(self) -> str:
		try:
			with winreg.OpenKey(self.hive, self.key_path) as key:
				value, _ = winreg.QueryValueEx(key, "PATH")
				return str(value)
		except FileNotFoundError:
			return ""
		except Exception as e:
			raise RuntimeError(f"Failed to read PATH: {e}") from e

	def _set(self, value: str) -> None:
		try:
			with winreg.OpenKey(self.hive, self.key_path, 0, winreg.KEY_WRITE) as key:
				winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, value)
		except Exception as e:
			raise RuntimeError(f"Failed to write PATH: {e}") from e

	def add(self, path: str) -> None:
		paths = self.all()
		if path not in paths:
			paths.append(path)
			self._set(';'.join(paths))

	def pop(self, path: str) -> None:
		paths = [p for p in self.all() if p != path]
		self._set(';'.join(paths))

	def all(self) -> list[str]:
		value = self.get()
		return [p.strip() for p in value.split(';') if p.strip()]

	def __iter__(self) -> Iterator[str]:
		return iter(self.all())
		
	def __contains__(self, path: str) -> bool:
		return path in self.all()

	def __len__(self) -> int:
		return len(self.all())

	def __getitem__(self, index: int|slice) -> str|list[str]:
		paths = self.all()
		return paths[index]

	def __repr__(self) -> str:
		return f"<PATH: {self.all()}>"

	def __str__(self) -> str:
		return self.get()