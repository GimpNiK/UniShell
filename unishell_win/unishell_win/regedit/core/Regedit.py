import winreg
import json
from typing import Optional, Union, List, Dict, Any

from reg_types import *
from reg_types import _REG_TYPE_AUTO, _REG_TYPE_INT,_REG_TYPE_STR

_HKEY_INT = {
    "HKCU": winreg.HKEY_CURRENT_USER,
    "HKU":  winreg.HKEY_USERS,
    "HKLM": winreg.HKEY_LOCAL_MACHINE,
    "HKCC": winreg.HKEY_CURRENT_CONFIG,
    "HKCR": winreg.HKEY_CLASSES_ROOT,
    "HKDD": winreg.HKEY_DYN_DATA,
    "HKPD": winreg.HKEY_PERFORMANCE_DATA
}

_HKEY_STR = {v: k for k, v in _HKEY_INT.items()}




class Container:
    """Registry container (key)"""
    
    def __init__(self, hive: int, path: str = ""):
        self.hive = hive
        self.path = path.strip("\\")
    
    def __truediv__(self, subpath: str) -> 'Container':
        
        if self.path:
            new_path = f"{self.path}\\{subpath}"
        else:
            new_path = subpath
        
        return Container(self.hive, new_path)
    
    def __getitem__(self, name: str) -> Optional[Any]:
        """Get field value"""
        field = Field(self, name)
        return field.get()
    
    def __setitem__(self, name: str, value: Any):
        """Set field value"""
        field = Field(self, name)
        field.set(value)
    
    def __delitem__(self, name: str):
        """Delete field"""
        field = Field(self, name)
        field.delete()
    
    def _open(self, access=winreg.KEY_READ):
        """Open registry key"""
        try:
            if self.path:
                return winreg.OpenKey(self.hive, self.path, 0, access)
            else:
                return winreg.OpenKey(self.hive, "", 0, access)
        except FileNotFoundError:
            raise FileNotFoundError(f"Container not found: {self.path}")
        except Exception as e:
            raise Exception(f"Error opening container: {e}")
    
    def create(self):
        """Create container"""
        try:
            if self.path:
                winreg.CreateKey(self.hive, self.path)
        except Exception as e:
            raise Exception(f"Error creating container: {e}")
    
    def delete(self, recursive: bool = True):
        if self.path:
            if recursive:
                for container_name in self.containers():
                    sub_container = self / container_name
                    sub_container.delete()
                
                for field_name in self.fields():
                    self[field_name] = None
                    del self[field_name]
            

            if not recursive:
                with self._open(winreg.KEY_READ):
                    subkeys = list(self.containers())
                    fields = list(self.fields())
                
                if subkeys or fields:
                    raise Exception("Container is not empty. Use delete(recursive=True) to force delete.")
            
            if "\\" in self.path:
                parent_path = "\\".join(self.path.split("\\")[:-1])
                key_name = self.path.split("\\")[-1]
                parent = Container(self.hive, parent_path)
                with parent._open(winreg.KEY_WRITE) as parent_key:
                    winreg.DeleteKey(parent_key, key_name)
            else:
                winreg.DeleteKey(self.hive, self.path)

    
    def rename(self, new_name: str):
        if "\\" in self.path:
            parent_path = "\\".join(self.path.split("\\")[:-1])
            parent = Container(self.hive, parent_path)
        else:
            parent = Container(self.hive, "")
        
        data = self.json()
        
        new_path = f"{parent.path}\\{new_name}" if parent.path else new_name
        new_container = Container(self.hive, new_path)
        new_container.create()
        
        new_container.from_json(data)
        
        old_container = Container(self.hive, self.path)
        old_container.delete()
        
        self.path = new_path
            

    
    def containers(self):
        try:
            with self._open() as key:
                i = 0
                while True:
                    try:
                        yield winreg.EnumKey(key, i)
                        i += 1
                    except OSError:
                        break
        except Exception:
            return []
    
    def fields(self):
        try:
            with self._open() as key:
                i = 0
                while True:
                    try:
                        name, _, _ = winreg.EnumValue(key, i)
                        yield name
                        i += 1
                    except OSError:
                        break
        except Exception:
            return []
    
    def json(self, use_types = False) -> Dict[str, Any]:
        """Export container to JSON"""
        result = {}
        
        for field_name in self.fields():
            field = Field(self, field_name)
            value = field.json(use_types = use_types)
            if value is not None:
                result[field_name] = value
        

        for container_name in self.containers():
            sub_container = self / container_name
            result[container_name] = sub_container.json(use_types = use_types)
                
        return result
    
    def from_json(self, data: Dict[str, Any], use_types = False):
        """Import container from JSON"""

        if not self.exists():
            self.create()
        
        for reg_el in data.keys():
            if not isinstance(data[reg_el], (dict)): # type is field
                field = Field(self,reg_el)
                field.from_json(data[reg_el], use_types = use_types)
            else:
                (self / reg_el).from_json(data[reg_el], use_types = use_types)
        
                

    
    def exists(self) -> bool:
        """Check if container exists"""
        try:
            with self._open():
                return True
        except Exception:
            return False
        
    def __repr__(self) -> str:
        return f"Container({_HKEY_STR[self.hive]}\\{self.path})"

class Field:
    """Registry field (value)"""
    
    def __init__(self, container: Container, name: str):
        self.container = container
        self.name = name
    
    def get(self,default = None, return_type = False) -> Optional[Any]:
        try:
            with self.container._open() as key:
                value, reg_type = winreg.QueryValueEx(key, self.name)
                if return_type:
                    return value,reg_type
                else:
                    return value  
        except FileNotFoundError:
            return default

    
    def set(self, value: Any, reg_type: Optional[int] = None):
        if reg_type is None:
            reg_type = _REG_TYPE_AUTO(value) 
        if reg_type == STRING:
            value = str(value)
        
        if not self.container.exists():
            self.container.create()
        
        with self.container._open(winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, self.name, 0, reg_type, value)
                

    
    def delete(self):
        try:
            with self.container._open(winreg.KEY_WRITE) as key:
                winreg.DeleteValue(key, self.name)
        except FileNotFoundError:
            pass 

    
    def exists(self) -> bool:
        try:
            with self.container._open() as key:
                winreg.QueryValueEx(key, self.name)
                return True
        except Exception:
            return False
    
    def rename(self, new_name: str):
        with self.container._open() as key:
            value, reg_type = winreg.QueryValueEx(key, self.name)
        
        with self.container._open(winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, new_name, 0, reg_type, value)
        
        self.delete()
    def type(self):
        if self.exists():
            with self.container._open() as key:
                _, reg_type = winreg.QueryValueEx(key, self.name)
                return _REG_TYPE_STR[reg_type]
        else:
            return None
    def json(self, use_types = False) ->  list[Any|str]|Any:
        ans = self.get(return_type = use_types)
        if use_types:
            value, reg_type = ans # type: ignore
            return value, _REG_TYPE_STR[reg_type]
        else:
            return ans
        
    def from_json(self, data, use_types = False):
        if use_types:
            value, reg_type = data
            reg_type = _REG_TYPE_INT[reg_type]
        else:
            value = data
            reg_type = None
        self.set(value, reg_type)
    def __repr__(self) -> str:
        return f"Field({self.container}\\{self.name})"




class Regedit:
    
    def __init__(self, hive: Union[int, str]):
        if isinstance(hive, str):
            hive = _HKEY_INT[hive.upper()]
        self.hive = hive
    
    def __truediv__(self, path: str) -> Container:
        return Container(self.hive, path)


# Example usage
if __name__ == "__main__":
    # 1. Create container
    container = Container(winreg.HKEY_CURRENT_USER, "SOFTWARE")
    
    # 2. Navigation with /
    test_container = container / "TestApp"
    
    # 3. Work with fields using type aliases
    field1 = Field(test_container, "field1")
    field2 = Field(test_container, "field2")
    field3 = Field(test_container, "field3")
    field4 = Field(test_container, "field4")
    field5 = Field(test_container, "field5")
    field6 = Field(test_container, "field6")
    # Set values with type aliases
    field1.set("String", STRING)  # String
    field2.set(42, INTEGER)  # 32-bit integer
    field3.set(9999999999, LONG_INT)  # 64-bit integer
    field4.set([ "string1", "string2" ], STRINGS)  # Multi-string
    field5.set(b'\x00\x01\x02', BINARY)  # Binary data
    field6.set("%PATH%", PATH)  # Expandable string
    
    # 4. Get value
    value = field1.get()
    print(f"Value: {value}, type: {type(value)}")
    
    # 5. Automatic type detection
    #field.set(100)  # Automatically detects as INTEGER
    #field.set("Text")  # Automatically detects as STRING
    #field.set([ "item1", "item2" ])  # Automatically detects as STRINGS
    
    # 6. Use Regedit for convenience
    reg = Regedit("HKCU")
    software = reg / "SOFTWARE" / "Microsoft" / "Windows"
    print(f"Path: {software.path}")
    

    
    # 8. Work with containers
    if test_container.exists():
        print(f"Container exists")
    
    # 9. List containers and fields
    print(f"Containers in SOFTWARE: {list(container.containers())[:5]}...")
    
    # 10. JSON export/import
    json_data = test_container.json()
    from pprint import pprint
    pprint(test_container.json(use_types=False))
    
    # Create new container from JSON
    new_container = container / "TestAppCopy"
    new_container.from_json(json_data, use_types = False)
    print()
    test_container["(По умолчанию)"] = [1,2]
    new_container.delete()
    test_container.delete()
    print()
