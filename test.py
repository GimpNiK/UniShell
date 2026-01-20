project_root = r"C:\Users\ПК\Desktop\UniShell\unishell"
import sys
sys.path.insert(0, project_root)
import unishell as uni

container = Container(HKEY_CURRENT_USER,key:str|"Container")
field = Field(container,name)
container = Regedit(HKEY_CURRENT_USER)/"SOFTWARE" # Container
zip_data = container/"7-zip" # если не является контейнером - ошибка

field = Field(zip_data, "Level")

field.get() # пайтон тип если не существует None
field.set(5,type = "DWORD") # по умолчанию определяется автоматически, создает контейнер и поле при необходимости
field.delete()

field.exists()
field.on_disk()
field.rename("new_name")

zip_data["Default"] # field.get() гарантировано Field or None
zip_data["Default"] = 5 #field.set()
del zip_data["Default"] #field.delete()


container.create()
container.delete()
container.rename("new_name")

container.containers() # содержимое пути(список  под путей) = ["AMD","7-zip"]
container.fields() # содержимое пути(список полей) = ["Level"]

temp = container.json() # возвращает рекурсивно содержимое для всех полей и ключей в формате json
container.from_json(temp)

