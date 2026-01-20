from typing import Iterator, TYPE_CHECKING, Any
from abc import ABC,abstractmethod
import winreg
if TYPE_CHECKING:
	from .UserType import UserTp

class RegDir:
	pass
class RegFile:
	pass



class RegPage(ABC):
	_regpath : str
	hive : int
	key : str
	def __init__(self, user: UserTp = None) -> None:
		from .UserType import _get_winreg_hkey, _get_winreg_subkey
		
		self.hive = _get_winreg_hkey(user)
		self.key = _get_winreg_subkey(user) + "\\" if _get_winreg_subkey(user) else "" + self._regpath
	
	@abstractmethod
	def get(self,name):
		""" Получает значение поля у ключа:
			HKEY_CURRENT_USER\SOFTWARE\7-Zip\Compression\Options\7z , Level -> 5
			Reg_SZ -> list
		"""
		...
	@abstractmethod
	def set(self,name): ...
	@abstractmethod
	def add(self,name): ...
	@abstractmethod
	def pop(self,name): ...
	
	
	def all(self): return dict(zip(self.keys(),self.values()))
	
		

	@abstractmethod	
	def keys(self) -> str:   ...
	def values(self):return [self.get(key) for key in self.keys()]

	def items(self):
		return list(zip(self.keys(), self.values()))
	
	def __getitem__(self,name): return self.get(name)
	def __delitem__(self,name): return self.pop(name)
	def __iter__(self):
		for name in self.keys():
			yield name
	def __contains__(self,name): return name in self.keys()
	def __len__(self): return len(self.keys())
	def __repr__(self): return f"<{self.__class__.__name__}> :" + str(self.all())
	def __str__(self): return str(self.all())