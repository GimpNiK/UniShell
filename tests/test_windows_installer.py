# from typing import Any, Dict, Optional

# class DictPointNotation:
#     """
#     Улучшенная версия с типами и валидацией
#     """
    
#     def __init__(self, data: Optional[Dict[str, Dict[str, Any]]] = None):
#         self._data: Dict[str, Dict[str, Any]] = data if data is not None else {}
#         self._current_key: Optional[str] = None
        
#     def __getitem__(self, key: str) -> 'DictPointNotation':
#         """Доступ через квадратные скобки"""
#         if not isinstance(key, str):
#             raise TypeError("Key must be a string")
            
#         self._current_key = key
#         if key not in self._data:
#             self._data[key] = {}
#         return self
    
#     def __setattr__(self, name: str, value: Any) -> None:
#         """Установка атрибутов"""
#         if name.startswith('_'):
#             super().__setattr__(name, value)
#         else:
#             if not hasattr(self, '_current_key') or self._current_key is None:
#                 raise AttributeError("Use object[key] syntax before setting attributes")
#             self._data[self._current_key][name] = value
#         return self
#     def field(self, field_name: str, value: Any) -> 'DictPointNotation':
#         """Установка поля через метод"""
#         if self._current_key is None:
#             raise AttributeError("Use object[key] syntax before setting fields")
#         self._data[self._current_key][field_name] = value
#         return self
    
#     @property
#     def json(self) -> Dict[str, Dict[str, Any]]:
#         """Данные только для чтения"""
#         return self._data.copy()
    
#     def get_for_key(self, key: str) -> Dict[str, Any]:
#         """Получение конфигурации для ключа"""
#         return self._data.get(key, {}).copy()
# FileType = DictPointNotation()
# ContextMenuDir = DictPointNotation()
# ContextMenuFile = DictPointNotation()

# NAME_PROJECT = "Project"
# VERSION_PROJECT  = "1.1.1"
# DIR_FROM_PROJECT = NAME_PROJECT
# DIR_FOR_PROJECT = "C:/Program files"

# MAIN_DIR = DIR_FOR_PROJECT + NAME_PROJECT

# ALL_USERS = False
# PATH = ["C:/Program files/my_project"]

# FileType[".txt"].run ="path" \
#                 .icon = "path"

# ContextMenuDir["Открыть в проводнике"].icon = "path" \
#                                       .posithion = "top|middle|bottom"

# ContextMenuFile["Открыть в проводнике"].icon = "path" \
#                                       .posithion = "top|middle|bottom"

# print(FileType.data)