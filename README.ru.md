# FileAlchemy

<<<<<<< HEAD
**FileAlchemy v. 1.1.1** — мощная и интуитивно понятная Python-библиотека для работы с файлами, директориями и текстовыми данными. Предоставляет два стиля API: shell-стиль с автоматическим расширением путей (UniShell) и Python-стиль (модуль structures).

## Два стиля API

### 1. UniShell — Shell-стиль с авторасширением путей
Высокоуровневый интерфейс, вдохновленный командной строкой Unix/Cmd. Автоматически расширяет пути с переменными окружения (`%VAR%`), специальными обозначениями (`~`, `..`, `.`), и поддерживает цепочки вызовов методов.

### 2. Structures — Python-стиль
Низкоуровневые классы для работы с файловой системой в объектно-ориентированном стиле. Полный контроль над операциями, без автоматического расширения путей.
=======
**FileAlchemy v. 1.1.1** — это мощная и интуитивно понятная Python-библиотека для работы с файлами, директориями и текстовыми данными. Она предоставляет удобный интерфейс для выполнения операций с файловой системой, обработки текста и управления кодировками, вдохновленный синтаксисом командной строки Unix и Cmd. Большинство названий команд дублирует функционал из этих двух командных оболочек. Предполагается использовать вместо bat и sh файлов, в интерактивном режиме использовать в Python Shell.

## Основные возможности

1. **Управление файлами и директориями**:
   - Создание, копирование, удаление, запись текста
   - Работа с архивами zip,tar,gztar,bztar,xztar (работает, используя модуль shutil).
   - Управление правами доступа (chmod)

2. **Работа с текстом**:
   - Чтение и запись файлов с автоматическим определением кодировки
   - Перекодировка между различными кодировками
   - Операции с текстом в памяти

3. **Удобный интерфейс**:
   - Цепочки вызовов методов
   - Перегрузка операторов >,>>,<,<< для работы с содержимым файлов 
   - Поддержка специальных путей (~, .., переменные окружения)

4. **Кроссплатформенность**:
   - Работает на Windows, Linux и macOS
   - Единый API для разных ОС
>>>>>>> origin/main

## Установка

```bash
pip install FileAlchemy
```

<<<<<<< HEAD
Для Windows-специфичных функций:
```bash
pip install FileAlchemy[windows]
```

**Требования:**
- Python 3.10+ (рекомендуется 3.11+)
- Основные зависимости: `chardet`, `py7zr`, `pyzipper`, `rarfile`
- Для Windows: `pywin32` (опционально, устанавливается с `[windows]`)

## Быстрый старт

### UniShell API (Shell-стиль)

```python
from FileAlchemy import UniShell

# Инициализация
shell = UniShell(
    current_dir=".",           # Начальная рабочая директория
    default_encoding="utf-8",   # Кодировка по умолчанию
    autodetect_encoding=False, # Автоопределение кодировки (требует chardet)
    sep="\n"                    # Разделитель для операций с несколькими файлами
)

# Автоматическое расширение путей
shell.file("~/documents/test.txt")  # Автоматически расширяет ~
shell.file("%CURRENTDIR%/data.txt") # Использует переменные окружения
shell.file("../parent/file.txt")    # Работает с относительными путями

# Работа с файлами
shell.file("test.txt").content = "Привет, мир!"
content = shell.file("test.txt").content

# Цепочки вызовов
shell.mkdir("backup").copy("data.txt", "backup/data.txt").make_archive("backup", "backup.zip")

# Работа с несколькими файлами
shell.files("1.txt", "2.txt", "3.txt") >> shell.file("combined.txt")
```

### Structures API (Python-стиль)

```python
from FileAlchemy.structures import File, Files, Dir, Archive
from pathlib import Path

# Работа с файлом
file = File("test.txt")
file.content = "Привет, мир!"
print(file.content)
print(file.sizeof())  # Размер в байтах
print(file.metadata())  # Все метаданные

# Работа с группой файлов
files = Files("1.txt", "2.txt", "3.txt", sep="\n---\n")
combined = files.content  # Объединенное содержимое

# Работа с директорией
dir = Dir("my_project")
dir.create()
for item in dir:  # Итерация по содержимому
    print(item)

# Работа с архивами
archive = Archive("data.zip")
archive.extract("extracted/")
archive.add_file("new_file.txt")
print(list(archive.list_files()))
=======
Требования:
- Python 3.8+
- Зависимости: `chardet` (для автоматического определения кодировок)

## Быстрый старт

```python
from FileAlchemy import CMD

# Инициализация
cmd = CMD()

# Изменение рабочей директории
cmd.cd("..")

# Создание файла и запись текста
cmd.file("test.txt").content = "Привет, мир!"

# Чтение файла
content = cmd.file("test.txt").content
print(content)  # "Привет, мир!"

#Сохранение содержимого нескольких файлов в один
cmd.files("1.txt","2.txt") >> cmd.file("3.txt")

#Очистка содержимого файла
del file("3.txt").content

# Копирование файла
cmd.copy("test.txt", "backup.txt")

# Работа с архивами
cmd.make_archive("backup.txt", "archive.zip")
>>>>>>> origin/main
```

## Подробное описание API

<<<<<<< HEAD
## UniShell API

### Инициализация

```python
shell = UniShell(
    sep="\n",                    # Разделитель для files()
    current_dir=os.getcwd(),     # Текущая рабочая директория
    default_encoding="utf-8",    # Кодировка по умолчанию
    autodetect_encoding=False,  # Автоопределение кодировки
    parms=ViewPort()            # Объект для переменных окружения
)
```

### Автоматическое расширение путей

UniShell автоматически расширяет пути:
- `~` → домашняя директория пользователя
- `..` → родительская директория текущей рабочей директории
- `.` → текущая рабочая директория
- `%VAR%` → переменные окружения из `shell.parms`

```python
shell.parms["MY_PATH"] = "/custom/path"
shell.file("%MY_PATH%/file.txt")  # Автоматически расширяется
```

### Методы UniShell

#### Создание объектов для работы с файлами

- **`file(path, encoding=None)`** → `File`
  - Создает объект File с автоматическим расширением пути
  - Если `encoding` не указана, используется `default_encoding` или автоопределение (если включено)

- **`files(*files, encoding=None, sep="\n")`** → `Files`
  - Создает объект Files для работы с группой файлов
  - `sep` — разделитель при объединении содержимого

#### Операции с файлами

- **`mkfile(path)` / `touch(path)`** — создание пустого файла
- **`rmfile(path)`** — удаление файла
- **`nano(path, edit_txt="notepad")`** — открытие файла в текстовом редакторе
- **`recode(file_path, to_encoding, from_encoding=None)`** — перекодирование файла

#### Операции с директориями

- **`mkdir(path, mode=0o777, parents=False, exist_ok=False)`** — создание директории
- **`rmdir(path)`** — удаление директории (рекурсивно)
- **`ls(path=".", details=False)`** — список файлов и директорий
  - Если `details=True`, возвращает словарь с метаданными

#### Операции с файлами и директориями

- **`copy(from_path, to_path, follow_symlinks=True)`** — копирование
- **`remove(path)` / `rm(path)`** — удаление файла или директории
- **`make(path, is_file=None)`** — создание полного пути (всех родительских директорий)
- **`chmod(path, mode)`** — изменение прав доступа

#### Работа с архивами

- **`make_archive(from_path, to_path=None, format="zip")`** / **`mkarch()`** / **`mk_archive()`**
  - Создание архива из файла или директории
  - Если `to_path` не указан, создается рядом с исходником

- **`extract_archive(archive_path, extract_dir=None, format=None)`** / **`unparch()`** / **`extarch()`**
  - Распаковка архива
  - Если `extract_dir` не указан, распаковывается в текущую директорию

#### Работа с путями

- **`cd(path)`** — изменение текущей рабочей директории
- **`to_abspath(path)`** — преобразование пути в абсолютный с расширением переменных

#### Переменные окружения (`shell.parms`)

- **`parms["VAR"] = value`** — установка локальной переменной
- **`parms.sets({"VAR1": val1, "VAR2": val2})`** — установка нескольких переменных
- **`parms.set_gl("VAR") = value`** — установка глобальной переменной
- **`parms.del("VAR")`** — удаление переменной
- **`parms.all()`** — список всех переменных

Все методы UniShell возвращают `self` для цепочек вызовов и имеют параметр `ignore_errors=False`.

### Псевдонимы методов UniShell

- `touch` = `mkfile`
- `rm` = `remove`
- `rmtree` = `rmdir`
- `mkarch` / `mk_archive` = `make_archive`
- `unparch` / `unp_arch` / `extarch` / `extarch` / `unpack_archive` = `extract_archive`
- `convert_encoding` = `recode`

## Structures API

### Класс File

Класс для работы с отдельным файлом.

#### Инициализация

```python
file = File(path, encoding=None)
# path может быть: str, Path, или другой объект File
```

#### Свойства

- **`content`** (str) — содержимое файла (чтение/запись/удаление)
  - При чтении автоматически определяет кодировку при ошибке
  - При записи автоматически выбирает минимальную подходящую кодировку
  - `del file.content` — очистка содержимого

- **`path`** (Path) — путь к файлу
- **`encoding`** (str) — кодировка файла
- **`name`** (str) — имя файла
- **`extension`** (str) — расширение файла (все суффиксы)
- **`parent`** (Dir) — родительская директория
- **`hidden`** (bool) — является ли файл скрытым

#### Методы

- **`create(mode=438, ignore_errors=True)`** — создание пустого файла
- **`remove()`** — удаление файла
- **`recode(to_encoding=None, from_encoding=None)`** — перекодирование
  - Если `to_encoding` не указана, определяется минимальная подходящая
- **`chmod(mode)`** — изменение прав доступа
- **`nano(edit_txt="notepad")`** — открытие в текстовом редакторе
- **`on_disk()`** → bool — существует ли файл на диске
- **`sizeof()`** → int — размер в байтах
- **`created_utc()`** → datetime — время создания (UTC)
- **`modified_utc()`** → datetime — время изменения (UTC)
- **`accessed_utc()`** → datetime — время доступа (UTC)
- **`created_lcl()`** → datetime — время создания (локальное)
- **`modified_lcl()`** → datetime — время изменения (локальное)
- **`accessed_lcl()`** → datetime — время доступа (локальное)
- **`is_symlink()`** → bool — является ли символьной ссылкой
- **`metadata()`** → dict — все метаданные файла

### Класс Files

Класс для работы с группой файлов.

#### Инициализация

```python
files = Files(*files, encoding=None, sep="\n")
# files может быть: str, Path, или File
```

#### Свойства

- **`content`** (str) — объединенное содержимое всех файлов через `sep`
- **`files`** (list[File]) — список объектов File
- **`sep`** (str) — разделитель

### Класс Dir

Класс для работы с директориями.

#### Инициализация

```python
dir = Dir(path)
# path может быть: str, Path, или другой объект Dir
```

#### Свойства

- **`path`** (Path) — путь к директории
- **`name`** (str) — имя директории (можно изменять)
- **`parent`** (Dir) — родительская директория (можно изменять для перемещения)
- **`hidden`** (bool) — является ли директория скрытой (можно изменять)

#### Методы

- **`create(mode=0o777, parents=False, ignore_errors=False)`** — создание директории
- **`add(path)`** — добавление файла или директории в директорию (копирование)
- **`move_to(dir)`** — перемещение директории
- **`rename(new_name)`** — переименование
- **`chmod(mode)`** — изменение прав доступа
- **`on_disk()`** → bool — существует ли директория
- **`sizeof(recursive=True, symlink=False)`** → int — размер в байтах
- **`len_files_and_dirs(recursive=True, symlinks=False)`** → dict — количество элементов
- **`created_utc()`** → datetime — время создания (UTC)
- **`modified_utc()`** → datetime — время изменения (UTC)
- **`accessed_utc()`** → datetime — время доступа (UTC)
- **`created_lcl()`** → datetime — время создания (локальное)
- **`modified_lcl()`** → datetime — время изменения (локальное)
- **`accessed_lcl()`** → datetime — время доступа (локальное)
- **`is_symlink()`** → bool — является ли символьной ссылкой
- **`metadata()`** → dict — все метаданные директории

#### Операторы

- **`dir / "filename"`** → File или Dir — доступ к файлу/поддиректории
- **`for item in dir:`** — итерация по содержимому (возвращает File или Dir)

### Класс Archive

Универсальный интерфейс для работы с архивами.

#### Поддерживаемые форматы

- **zip** — создание, добавление, извлечение (с паролями через pyzipper)
- **7z** — создание, добавление, извлечение (с паролями)
- **tar** — создание, добавление, извлечение
- **tar.gz / tgz** — создание, добавление, извлечение
- **tar.bz2 / tbz2** — создание, добавление, извлечение
- **gz** — только чтение и извлечение (один файл)
- **bz2** — только чтение и извлечение (один файл)
- **rar** — только чтение и извлечение (с паролями, требует rarfile)

#### Инициализация

```python
archive = Archive(path, format=None, password=None)
# format определяется автоматически по расширению, если не указан
```

#### Методы

- **`add(path, arcname=None)`** — добавление файла или директории в архив
- **`extract(path, member=None)`** — извлечение архива или конкретного элемента
- **`list_files()`** → list[str] — список файлов в архиве
- **`create()`** — создание пустого архива
- **`cleanup()`** — удаление временных файлов (для 7z и tar)

#### Класс-методы

- **`Archive.create_from(path, format, files, password=None)`** — создание архива с файлами

#### Итерация

```python
for filename in archive:
    print(filename)  # Имена файлов в архиве
```

## Операторы потоков (>>, >, <<, <)

Классы `File` и `Files` поддерживают операторы для работы с содержимым:

- **`a > b`** — копирует содержимое `a` в `b` (перезаписывает `b`)
- **`a >> b`** — добавляет содержимое `a` в конец `b` (с учетом `sep`)
- **`a < b`** — копирует содержимое `b` в `a` (перезаписывает `a`)
- **`a << b`** — добавляет содержимое `b` в конец `a` (с учетом `sep`)

```python
from FileAlchemy.structures import File, Files

file1 = File("a.txt")
file2 = File("b.txt")
file1 > file2  # Копирует содержимое a.txt в b.txt

files = Files("1.txt", "2.txt")
combined = File("combined.txt")
files >> combined  # Добавляет содержимое всех файлов в combined.txt
=======
### Инициализация

```python
cmd = CMD(
    sep="\n",               # Разделитель по умолчанию для операций с текстом
    current_dir=".",        # Начальная рабочая директория(по умолчанию, места нахождения проекта)
    default_encoding="utf-8" # Кодировка по умолчанию
)
```

### Основные методы

#### Работа с файлами

- `file(path)` - создает объект для работы с файлом
- `files(*paths)` - создает объект для работы с группой файлов
- `text(content="")` - создает объект для работы с текстом


#### Операции с файлами(методы CMD)
- `mkfile(path) / touch(path)` - создание пустого файла
- `rmfile(path)` - удаление файла
- `nano(path)` - открытие файла в текстовом редакторе
- `recode(path, to_encoding = min_encoding, from_encoding = realy_encoding)` - перекодирование файла(если не указаны необязательные параметры файл перезаписывается в минимально возможную кодировку)

#### Операции с папками (методы CMD)
- `mkdir(path)` - создание директории
- `rmdir(path)` - удаление директории

#### Операции с папками/файлами (методы CMD)
- `copy(from_path, to_path)` - копирование файла/директории
- `make(path)` - создание полного пути
- `rm(path)` - удаление папки/файла
- `mkarch(from_path, to_path) / make_archive` - создание архива папки/файла
- `unpack_archive(archive_path, extract_dir) / unparch` - распаковка архива папки/файла
- `chmod(path, mode)` - изменение прав доступа папки/файла

#### Работа с путями
- `to_abspath(path)` - преобразование в абсолютный путь
- `cd(path)` - изменение текущей директории
- `ls(details = False)` - выводит список файлов в директории

#### Работа с переменными окружения(CMD().parms)
- `set_gl `- устанвливает значение глобальной перменной(str)
- `del_gl `  - удаляет значение глобальной перменной
- `set   `   - устанавливает значение локальной переменной
- `sets `    - устанавливает значения локальных переменных(dict)
- `del  `    - удаляет значение локальной переменной
- `dels `    - удаляет значения локальных переменных (list)

Все переменные окружения подставляются в пути:
```python
#Создаем экземпляр командной строки
cmd = CMD()
#Создаем переменную окружения
my_var = cmd.parms["~"]
cmd.parms["my_var"] = my_var #локальную по значению
cmd.parms["my var"] = lambda: my_var # локальную по ссылке
cmd.parms.set_gl("my_var") = my_var # глобальную по значению
cmd.ls(path = "%my_var%") #выведет список файлов в домашней директории
```
### Перегрузка операторов

Библиотека предоставляет удобные операторы для работы с содержимым:

```python
# Перезапись содержимого
cmd.file("a.txt") > cmd.file("b.txt")  # a.txt → b.txt
cmd.file("b.txt") < cmd.file("a.txt")  # b.txt ← a.txt

# Добавление содержимого
cmd.file("1and2.txt") << cmd.files("1.txt","2.txt")
cmd.file("log.txt") << cmd.text("новая запись")  # добавление в конец
```

### Управление кодировками

Библиотека автоматически определяет кодировки файлов и предоставляет методы для работы с ними:

```python
# Автоматическое определение кодировки
file_obj = cmd.file("unknown.txt")
print(file_obj.encoding)  # например, "utf-8" или "cp1251"

# Перекодировка файла
file_obj.recode("utf-8")

# Определение минимальной подходящей кодировки
min_encoding = cmd.determine_minimal_encoding("Текст")
>>>>>>> origin/main
```

## Примеры использования

<<<<<<< HEAD
### Пример 1: Резервное копирование (UniShell)

```python
from FileAlchemy import UniShell
import datetime

shell = UniShell()
today = datetime.datetime.now().strftime("%Y-%m-%d")
shell.make_archive("project", f"backups/project_{today}.zip")
```

### Пример 2: Логирование (Structures)

```python
from FileAlchemy.structures import File
import datetime

log_file = File("app.log")
log_entry = f"{datetime.datetime.now()}: Новое событие\n"
log_file.content = log_file.content + log_entry
```

### Пример 3: Работа с конфигурационными файлами (UniShell)

```python
from FileAlchemy import UniShell
import json

shell = UniShell()
config = shell.file("config.json").content
settings = json.loads(config)
settings["timeout"] = 30
shell.file("config.json").content = json.dumps(settings, indent=2)
```

### Пример 4: Обработка нескольких файлов (Structures)

```python
from FileAlchemy.structures import Files, File

files = Files("file1.txt", "file2.txt", "file3.txt", sep="\n---\n")
all_content = files.content  # Объединенное содержимое
File("combined.txt").content = all_content
```

### Пример 5: Работа с архивами (Structures)

```python
from FileAlchemy.structures import Archive

# Создание архива
archive = Archive("backup.zip")
archive.add("file1.txt")
archive.add("directory/")

# Извлечение
archive.extract("extracted/")

# Список файлов
print(archive.list_files())
```

## Windows-специфичные функции

Модуль `FileAlchemy.Windows.regedit` предоставляет работу с реестром Windows и учетными записями (требует `pywin32`):

```python
from FileAlchemy.Windows.regedit import CurrentUser, User, Users, PATH, AutoRun

# Текущий пользователь
cur_user = CurrentUser()
print(cur_user.PATH.all())  # PATH текущего пользователя

# Работа с PATH
cur_user.PATH.add("C:/new/path")
cur_user.PATH.pop("C:/old/path")

# Автозапуск
cur_user.AutoRun.add("MyApp", "C:/app.exe")
cur_user.AutoRun.remove("MyApp")

# Работа с пользователями
user = User(name="username")
users = Users.local()  # Список локальных пользователей
=======

### 1. Создание резервных копий

```python
# Создание архива с текущей датой
import datetime
today = datetime.datetime.now().strftime("%Y-%m-%d")
cmd.make_archive("project", f"backups/project_{today}.zip")
```

### 2. Логирование

```python
# Добавление записи в лог-файл
log_entry = f"{datetime.datetime.now()}: Новое событие\n"
cmd.file("app.log") << cmd.text(log_entry)
```

### 3. Работа с конфигурационными файлами

```python
# Чтение конфига
config = cmd.file("config.json").content
import json
settings = json.loads(config)

# Изменение и сохранение
settings["timeout"] = 30
cmd.file("config.json").content = json.dumps(settings, indent=2)
>>>>>>> origin/main
```

## Особенности реализации

<<<<<<< HEAD
1. **Ленивые операции** — файлы читаются только при необходимости
2. **Автовосстановление** — автоматическое определение кодировки при ошибках чтения
3. **Безопасность** — проверка существования файлов перед операциями
4. **Кроссплатформенность** — единое API для Windows, Linux и macOS
5. **Два уровня API** — shell-стиль (UniShell) и Python-стиль (structures)
6. **Потоковые операции** — поддержка операторов >>, >, <<, < для работы с содержимым

## Лицензия

FileAlchemy распространяется под **MIT License**. Смотрите файл LICENSE для подробностей.

### Лицензии зависимостей

Проект использует следующие зависимости с их лицензиями:

- **chardet** — LGPL
- **py7zr** — LGPL-2.1-or-later
- **pyzipper** — MIT
- **rarfile** — ISC
- **pywin32** (опционально) — PSF (Python Software Foundation License)

Все зависимости совместимы с MIT License. Подробную информацию см. в файле [LICENSES_DEPENDENCIES.md](LICENSES_DEPENDENCIES.md).

## Автор

GimpNiK (https://github.com/GimpNiK) — разработчик и maintainer проекта.
=======
1. **Ленивые операции** - файлы читаются только при необходимости
2. **Автовосстановление** - автоматическое определение кодировки при ошибках чтения
3. **Безопасность** - проверка существования файлов перед операциями
4. **Кроссплатформенность** - единое API для разных операционных систем

**В процессе разработки:** 
1. Ускорение чтения и записи за счет снятия ожидания конца записи, множественное чтение(threading).
2. Оптимизация регулярок для поиска файлов.
3. Улучшение работы с архивами.

## Лицензия

MIT License. Смотрите файл LICENSE для подробностей.



## Автор

GimpNiK (https://github.com/GimpNiK) - разработчик и maintainer проекта.

# Полная документация

## Описание

Класс `CMD` — основной интерфейс для работы с файлами, текстом и директориями. Предоставляет методы для управления файлами, директориями, кодировками, а также вспомогательные классы для работы с содержимым.

---

## Методы класса CMD

### text(content: str = "", encoding: Optional[str] = None) -> _text
Создаёт объект _text для работы с текстом в памяти.
- **content** (`str`): исходный текст
- **encoding** (`str | None`): кодировка (по умолчанию — default_encoding)
- **return**: объект _text

### file(path: str | Path, encoding: Optional[str] = None) -> _file
Создаёт объект _file для работы с файлом.
- **path** (`str | Path`): путь к файлу
- **encoding** (`str | None`): кодировка (определяется автоматически, если не указана)
- **return**: объект _file

### files(*args, encoding: Optional[str] = None) -> _files
Создаёт объект _files для работы с группой файлов.
- **args** (`str | Path | _file`): пути к файлам или объекты _file
- **encoding** (`str | None`): кодировка (по умолчанию — default_encoding)
- **return**: объект _files

### cd(path: str | Path) -> CMD
Меняет текущую рабочую директорию.
- **path** (`str | Path`): новый путь
- **return**: self (для цепочек вызовов)

### copy(from_path: str | Path, to_path: str | Path, *, follow_symlinks: bool = True, ignore_errors: bool = False) -> CMD
Копирует файл или директорию.
- **from_path** (`str | Path`): исходный путь
- **to_path** (`str | Path`): куда копировать
- **follow_symlinks** (`bool`): следовать за символическими ссылками
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### mkdir(path: str | Path, mode: int = 0o777, parents: bool = False, exist_ok: bool = False, ignore_errors: bool = False) -> CMD
Создаёт директорию.
- **path** (`str | Path`): путь к директории
- **mode** (`int`): права доступа
- **parents** (`bool`): создавать родительские директории
- **exist_ok** (`bool`): не выдавать ошибку, если директория уже существует
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### mkfile(path: str | Path, ignore_errors: bool = False) -> CMD
Создаёт пустой файл.
- **path** (`str | Path`): путь к файлу
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### rmfile(path: str | Path, ignore_errors: bool = False) -> CMD
Удаляет файл.
- **path** (`str | Path`): путь к файлу
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### rmdir(path: str | Path, ignore_errors: bool = False, onerror=None) -> CMD
Рекурсивно удаляет директорию.
- **path** (`str | Path`): путь к директории
- **ignore_errors** (`bool`): игнорировать ошибки
- **onerror** (`callable | None`): обработчик ошибок
- **return**: self

### make_archive(from_path: str | Path, to_path: str | Path | None = None, format: str = "zip", owner: Optional[str] = None, group: Optional[str] = None, ignore_errors: bool = False) -> CMD
Создаёт архив из файла или директории.
- **from_path** (`str | Path`): что архивировать
- **to_path** (`str | Path | None`): куда сохранить архив (по умолчанию — рядом с исходником)
- **format** (`str`): формат архива (zip, tar и др.)
- **owner** (`str | None`): владелец (опционально)
- **group** (`str | None`): группа (опционально)
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### extract_archive(archive_path: str | Path, extract_dir: Optional[str | Path] = None, format: Optional[str] = None, ignore_errors: bool = False) -> CMD
Распаковывает архив в директорию.
- **archive_path** (`str | Path`): путь к архиву
- **extract_dir** (`str | Path | None`): куда распаковать (по умолчанию — текущая директория)
- **format** (`str | None`): формат архива (опционально)
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### chmod(path: str | Path, mode: int, ignore_errors: bool = False) -> CMD
Меняет права доступа к файлу или директории.
- **path** (`str | Path`): путь
- **mode** (`int`): новый режим (например, 0o755)
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### recode(file_path: str | Path, to_encoding: str, from_encoding: Optional[str] = None, ignore_errors: bool = False) -> CMD
Перекодирует файл в другую кодировку.
- **file_path** (`str | Path`): путь к файлу
- **to_encoding** (`str`): целевая кодировка
- **from_encoding** (`str | None`): исходная кодировка (опционально)
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### nano(path: str | Path, edit_txt="notepad", ignore_errors: bool = False) -> CMD
Открывает файл в текстовом редакторе.
- **path** (`str | Path`): путь к файлу
- **edit_txt** (`str`): имя редактора (по умолчанию notepad)
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### remove(path: str | Path, ignore_errors: bool = False) -> CMD
Удаляет файл или директорию рекурсивно.
- **path** (`str | Path`): путь
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### make(path: str | Path, is_file: bool = None, ignore_errors: bool = False) -> CMD
Создаёт все папки в пути и, если нужно, файл.
- **path** (`str | Path`): путь
- **is_file** (`bool | None`): является ли путь файлом
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### ls(path: str | Path = ".", details: bool = False, ignore_errors: bool = False)
Список файлов и директорий в указанном пути.
- **path** (`str | Path`): путь
- **details** (`bool`): возвращать подробную информацию
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: список файлов или словарь с деталями

---

## Операции потоков (>>, >, <<, <) с файлами и текстом

Класс CMD поддерживает удобные операторы для передачи и объединения содержимого между файлами и текстовыми объектами:

- `a > b` — копирует содержимое объекта `a` в объект `b` (перезаписывает содержимое `b`).
- `a >> b` — добавляет содержимое объекта `a` в конец объекта `b` (с учётом разделителя `sep`).
- `a < b` — копирует содержимое объекта `b` в объект `a` (перезаписывает содержимое `a`).
- `a << b` — добавляет содержимое объекта `b` в конец объекта `a` (с учётом разделителя `sep`).

>>>>>>> origin/main
