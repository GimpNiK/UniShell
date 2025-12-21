# FileAlchemy

**FileAlchemy v. 1.1.1** — это мощная и интуитивно понятная Python-библиотека для работы с файлами, директориями и текстовыми данными. Она предоставляет удобный интерфейс для выполнения операций с файловой системой, обработки текста и управления кодировками, вдохновленный синтаксисом командной строки Unix и Cmd. Большинство названий команд дублирует функционал из этих двух командных оболочек. Предполагается использовать вместо bat и sh файлов, в интерактивном режиме использовать в Python Shell.

## Основные модули:    
1. **UniShell (основной класс)** — высокоуровневый интерфейс для работы с файлами и директориями
   - Управление файлами, директориями, архивами
   - Работа с кодировками
   - Перегрузка операторов для удобной работы с содержимым

2. **structures** — низкоуровневые классы для работы с файловой системой
   - `File` — класс для работы с отдельным файлом
   - `Files` — класс для работы с группой файлов
   - `Dir` — класс для работы с директориями
   - `Archive` — универсальный класс для работы с архивами (zip, 7z, tar, rar и др.)
   - `Stream` — базовый класс для потоковых операций

3. **Кодировки** — автоматическое определение и перекодировка файлов

4. **Реестр Windows и учетные записи** (только Windows)
   - Создание, просмотр, удаление учетных записей 
   - Редактирование и просмотр PATH, Run, RunOnce

## Основные возможности

1. **Управление файлами и директориями**:
   - Создание, копирование, удаление, запись текста
   - Работа с архивами: zip, 7z, tar, tar.gz, tar.bz2, rar, gz, bz2
   - Управление правами доступа (chmod)
   - Получение метаданных файлов (размер, даты создания/изменения, скрытость и т.д.)

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

## Установка

```bash
pip install FileAlchemy
```

Требования:
- Python 3.10+ (рекомендуется 3.11+)
- Зависимости: 
  - `chardet` (для автоматического определения кодировок)
  - Для работы с архивами: `py7zr`, `rarfile` (опционально)
  - Для Windows функций: `pywin32` (опционально)

## Быстрый старт

### Использование класса UniShell (высокоуровневый API)

```python
from FileAlchemy import UniShell

# Инициализация
shell = UniShell()

# Изменение рабочей директории
shell.cd("..")

# Создание файла и запись текста
shell.file("test.txt").content = "Привет, мир!"

# Чтение файла
content = shell.file("test.txt").content
print(content)  # "Привет, мир!"

# Сохранение содержимого нескольких файлов в один
shell.files("1.txt","2.txt") >> shell.file("3.txt")

# Очистка содержимого файла
del shell.file("3.txt").content

# Копирование файла
shell.copy("test.txt", "backup.txt")

# Работа с архивами
shell.make_archive("backup.txt", "archive.zip")
```

### Использование модуля structures (низкоуровневый API)

```python
from FileAlchemy.structures import File, Files, Dir, Archive

# Работа с файлом
file = File("test.txt")
file.content = "Привет, мир!"
print(file.content)

# Работа с группой файлов
files = Files("1.txt", "2.txt", "3.txt")
combined_content = files.content  # Объединенное содержимое

# Работа с директорией
dir = Dir("my_folder")
dir.create()
for item in dir:  # Итерация по файлам и папкам
    print(item)

# Работа с архивами
archive = Archive("data.zip")
archive.extract("extracted/")
archive.add_file("new_file.txt")
```

## Подробное описание API

### Инициализация

```python
shell = UniShell(
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


#### Операции с файлами(методы UniShell)
- `mkfile(path) / touch(path)` - создание пустого файла
- `rmfile(path)` - удаление файла
- `nano(path)` - открытие файла в текстовом редакторе
- `recode(path, to_encoding = min_encoding, from_encoding = realy_encoding)` - перекодирование файла(если не указаны необязательные параметры файл перезаписывается в минимально возможную кодировку)

#### Операции с папками (методы UniShell)
- `mkdir(path)` - создание директории
- `rmdir(path)` - удаление директории

#### Операции с папками/файлами (методы UniShell)
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

#### Работа с переменными окружения(UniShell().parms)
- `set_gl `- устанвливает значение глобальной перменной(str)
- `del_gl `  - удаляет значение глобальной перменной
- `set   `   - устанавливает значение локальной переменной
- `sets `    - устанавливает значения локальных переменных(dict)
- `del  `    - удаляет значение локальной переменной
- `dels `    - удаляет значения локальных переменных (list)

Все переменные окружения подставляются в пути:
```python
#Создаем экземпляр командной строки
shell = UniShell()
#Создаем переменную окружения
my_var = shell.parms["~"]
shell.parms["my_var"] = my_var #локальную по значению
shell.parms["my var"] = lambda: my_var # локальную по ссылке
shell.parms.set_gl("my_var") = my_var # глобальную по значению
shell.ls(path = "%my_var%") #выведет список файлов в домашней директории
```
### Перегрузка операторов

Библиотека предоставляет удобные операторы для работы с содержимым:

```python
# Перезапись содержимого
shell.file("a.txt") > shell.file("b.txt")  # a.txt → b.txt
shell.file("b.txt") < shell.file("a.txt")  # b.txt ← a.txt

# Добавление содержимого
shell.file("1and2.txt") << shell.files("1.txt","2.txt")
# Примечание: операторы работают с объектами File и Files из модуля structures
```

### Управление кодировками

Библиотека автоматически определяет кодировки файлов и предоставляет методы для работы с ними:

```python
# Автоматическое определение кодировки
file_obj = shell.file("unknown.txt")
print(file_obj.encoding)  # например, "utf-8" или "cp1251"

# Перекодировка файла
file_obj.recode("utf-8")

# Определение минимальной подходящей кодировки
from FileAlchemy.encoding_utils import determine_minimal_encoding
min_encoding = determine_minimal_encoding("Текст")
```

## Примеры использования


### 1. Создание резервных копий

```python
# Создание архива с текущей датой
import datetime
from FileAlchemy import UniShell

shell = UniShell()
today = datetime.datetime.now().strftime("%Y-%m-%d")
shell.make_archive("project", f"backups/project_{today}.zip")
```

### 2. Логирование

```python
from FileAlchemy import UniShell
from FileAlchemy.structures import File, Files

shell = UniShell()
# Добавление записи в лог-файл
log_entry = f"{datetime.datetime.now()}: Новое событие\n"
log_file = shell.file("app.log")
log_file.content = log_file.content + log_entry
```

### 3. Работа с конфигурационными файлами

```python
from FileAlchemy import UniShell
import json

shell = UniShell()
# Чтение конфига
config = shell.file("config.json").content
settings = json.loads(config)

# Изменение и сохранение
settings["timeout"] = 30
shell.file("config.json").content = json.dumps(settings, indent=2)
```

### 4. Использование модуля structures

```python
from FileAlchemy.structures import File, Files, Dir, Archive

# Работа с одним файлом
file = File("data.txt")
file.content = "Новые данные"
print(f"Размер файла: {file.sizeof()} байт")
print(f"Создан: {file.created_lcl()}")

# Работа с несколькими файлами
files = Files("file1.txt", "file2.txt", "file3.txt", sep="\n---\n")
all_content = files.content  # Объединенное содержимое

# Работа с директориями
dir = Dir("my_project")
dir.create()
print(f"Количество файлов: {dir.len_files_and_dirs()['files']}")
print(f"Размер директории: {dir.sizeof()} байт")

# Работа с архивами
archive = Archive("backup.zip")
archive.extract("extracted/")
archive.add_file("new_file.txt")
print(f"Файлы в архиве: {list(archive.list_files())}")
```

## Особенности реализации

1. **Ленивые операции** - файлы читаются только при необходимости
2. **Автовосстановление** - автоматическое определение кодировки при ошибках чтения
3. **Безопасность** - проверка существования файлов перед операциями
4. **Кроссплатформенность** - единое API для разных операционных систем
5. **Два уровня API** - высокоуровневый (UniShell) и низкоуровневый (structures)
6. **Потоковые операции** - поддержка операторов >>, >, <<, < для работы с содержимым

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

Класс `UniShell` — основной интерфейс для работы с файлами, текстом и директориями. Предоставляет методы для управления файлами, директориями, кодировками, а также работу с классами из модуля structures.

---

## Методы класса UniShell

### file(path: str | Path, encoding: Optional[str] = None) -> File
Создаёт объект File для работы с файлом.
- **path** (`str | Path`): путь к файлу
- **encoding** (`str | None`): кодировка (определяется автоматически, если не указана)
- **return**: объект File из модуля structures

### files(*files: str | Path | File, encoding: Optional[str] = None, sep: str = "\n") -> Files
Создаёт объект Files для работы с группой файлов.
- **files** (`str | Path | File`): пути к файлам или объекты File
- **encoding** (`str | None`): кодировка (по умолчанию — default_encoding)
- **sep** (`str`): разделитель для объединения содержимого
- **return**: объект Files из модуля structures

### cd(path: str | Path) -> UniShell
Меняет текущую рабочую директорию.
- **path** (`str | Path`): новый путь
- **return**: self (для цепочек вызовов)

### copy(from_path: str | Path, to_path: str | Path, *, follow_symlinks: bool = True, ignore_errors: bool = False) -> UniShell
Копирует файл или директорию.
- **from_path** (`str | Path`): исходный путь
- **to_path** (`str | Path`): куда копировать
- **follow_symlinks** (`bool`): следовать за символическими ссылками
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### mkdir(path: str | Path, mode: int = 0o777, parents: bool = False, exist_ok: bool = False, ignore_errors: bool = False) -> UniShell
Создаёт директорию.
- **path** (`str | Path`): путь к директории
- **mode** (`int`): права доступа
- **parents** (`bool`): создавать родительские директории
- **exist_ok** (`bool`): не выдавать ошибку, если директория уже существует
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### mkfile(path: str | Path, ignore_errors: bool = False) -> UniShell
Создаёт пустой файл.
- **path** (`str | Path`): путь к файлу
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### rmfile(path: str | Path, ignore_errors: bool = False) -> UniShell
Удаляет файл.
- **path** (`str | Path`): путь к файлу
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### rmdir(path: str | Path, ignore_errors: bool = False, onexc=None) -> UniShell
Рекурсивно удаляет директорию.
- **path** (`str | Path`): путь к директории
- **ignore_errors** (`bool`): игнорировать ошибки
- **onexc** (`callable | None`): обработчик ошибок
- **return**: self

### make_archive(from_path: str | Path, to_path: str | Path | None = None, format: str = "zip", owner: Optional[str] = None, group: Optional[str] = None, ignore_errors: bool = False) -> UniShell
Создаёт архив из файла или директории.
- **from_path** (`str | Path`): что архивировать
- **to_path** (`str | Path | None`): куда сохранить архив (по умолчанию — рядом с исходником)
- **format** (`str`): формат архива (zip, tar и др.)
- **owner** (`str | None`): владелец (опционально)
- **group** (`str | None`): группа (опционально)
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### extract_archive(archive_path: str | Path, extract_dir: Optional[str | Path] = None, format: Optional[str] = None, ignore_errors: bool = False) -> UniShell
Распаковывает архив в директорию.
- **archive_path** (`str | Path`): путь к архиву
- **extract_dir** (`str | Path | None`): куда распаковать (по умолчанию — текущая директория)
- **format** (`str | None`): формат архива (опционально)
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### chmod(path: str | Path, mode: int, ignore_errors: bool = False) -> UniShell
Меняет права доступа к файлу или директории.
- **path** (`str | Path`): путь
- **mode** (`int`): новый режим (например, 0o755)
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### recode(file_path: str | Path, to_encoding: str, from_encoding: Optional[str] = None, ignore_errors: bool = False) -> UniShell
Перекодирует файл в другую кодировку.
- **file_path** (`str | Path`): путь к файлу
- **to_encoding** (`str`): целевая кодировка
- **from_encoding** (`str | None`): исходная кодировка (опционально)
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### nano(path: str | Path, edit_txt="notepad", ignore_errors: bool = False) -> UniShell
Открывает файл в текстовом редакторе.
- **path** (`str | Path`): путь к файлу
- **edit_txt** (`str`): имя редактора (по умолчанию notepad)
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### remove(path: str | Path, ignore_errors: bool = False) -> UniShell
Удаляет файл или директорию рекурсивно.
- **path** (`str | Path`): путь
- **ignore_errors** (`bool`): игнорировать ошибки
- **return**: self

### make(path: str | Path, is_file: bool = None, ignore_errors: bool = False) -> UniShell
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

## Операции потоков (>>, >, <<, <) с файлами

Классы File и Files из модуля structures поддерживают удобные операторы для передачи и объединения содержимого:

- `a > b` — копирует содержимое объекта `a` в объект `b` (перезаписывает содержимое `b`).
- `a >> b` — добавляет содержимое объекта `a` в конец объекта `b` (с учётом разделителя `sep`).
- `a < b` — копирует содержимое объекта `b` в объект `a` (перезаписывает содержимое `a`).
- `a << b` — добавляет содержимое объекта `b` в конец объекта `a` (с учётом разделителя `sep`).

Пример:
```python
from FileAlchemy.structures import File, Files

file1 = File("a.txt")
file2 = File("b.txt")
file1 > file2  # Копирует содержимое a.txt в b.txt

files = Files("1.txt", "2.txt")
combined = File("combined.txt")
files >> combined  # Добавляет содержимое всех файлов в combined.txt
```

