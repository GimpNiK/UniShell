# FileAlchemy

**FileAlchemy v. 1.1.1** — мощная и интуитивно понятная Python-библиотека для работы с файлами, директориями и текстовыми данными. Предоставляет два стиля API: shell-стиль с автоматическим расширением путей (UniShell) и Python-стиль (модуль structures).

## Два стиля API

### 1. UniShell — Shell-стиль с авторасширением путей
Высокоуровневый интерфейс, вдохновленный командной строкой Unix/Cmd. Автоматически расширяет пути с переменными окружения (`%VAR%`), специальными обозначениями (`~`, `..`, `.`), и поддерживает цепочки вызовов методов.

### 2. Structures — Python-стиль
Низкоуровневые классы для работы с файловой системой в объектно-ориентированном стиле. Полный контроль над операциями, без автоматического расширения путей.

## Установка

```bash
pip install FileAlchemy
```

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
```

## Подробное описание API

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
```

## Примеры использования

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
```

## Особенности реализации

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
