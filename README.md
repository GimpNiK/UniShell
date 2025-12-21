# FileAlchemy

**FileAlchemy v. 1.1.1** — A powerful and intuitive Python library for working with files, directories, and text data. Provides two API styles: shell-style with automatic path expansion (UniShell) and Python-style (structures module).

## Two API Styles

### 1. UniShell — Shell-style with Automatic Path Expansion
High-level interface inspired by Unix/Cmd command-line. Automatically expands paths with environment variables (`%VAR%`), special notations (`~`, `..`, `.`), and supports method chaining.

### 2. Structures — Python-style
Low-level classes for file system operations in object-oriented style. Full control over operations, without automatic path expansion.

## Installation

```bash
pip install FileAlchemy
```

For Windows-specific features:
```bash
pip install FileAlchemy[windows]
```

**Requirements:**
- Python 3.10+ (3.11+ recommended)
- Core dependencies: `chardet`, `py7zr`, `pyzipper`, `rarfile`
- For Windows: `pywin32` (optional, install with `[windows]`)

## Quick Start

### UniShell API (Shell-style)

```python
from FileAlchemy import UniShell

# Initialization
shell = UniShell(
    current_dir=".",           # Initial working directory
    default_encoding="utf-8",   # Default encoding
    autodetect_encoding=False, # Auto-detect encoding (requires chardet)
    sep="\n"                    # Separator for multi-file operations
)

# Automatic path expansion
shell.file("~/documents/test.txt")  # Automatically expands ~
shell.file("%CURRENTDIR%/data.txt") # Uses environment variables
shell.file("../parent/file.txt")    # Works with relative paths

# Working with files
shell.file("test.txt").content = "Hello, world!"
content = shell.file("test.txt").content

# Method chaining
shell.mkdir("backup").copy("data.txt", "backup/data.txt").make_archive("backup", "backup.zip")

# Working with multiple files
shell.files("1.txt", "2.txt", "3.txt") >> shell.file("combined.txt")
```

### Structures API (Python-style)

```python
from FileAlchemy.structures import File, Files, Dir, Archive
from pathlib import Path

# Working with file
file = File("test.txt")
file.content = "Hello, world!"
print(file.content)
print(file.sizeof())  # Size in bytes
print(file.metadata())  # All metadata

# Working with multiple files
files = Files("1.txt", "2.txt", "3.txt", sep="\n---\n")
combined = files.content  # Combined content

# Working with directory
dir = Dir("my_project")
dir.create()
for item in dir:  # Iterate over contents
    print(item)

# Working with archives
archive = Archive("data.zip")
archive.extract("extracted/")
archive.add("new_file.txt")
print(list(archive.list_files()))
```

## Detailed API Documentation

## UniShell API

### Initialization

```python
shell = UniShell(
    sep="\n",                    # Separator for files()
    current_dir=os.getcwd(),     # Current working directory
    default_encoding="utf-8",    # Default encoding
    autodetect_encoding=False,  # Auto-detect encoding
    parms=ViewPort()            # Environment variables object
)
```

### Automatic Path Expansion

UniShell automatically expands paths:
- `~` → user's home directory
- `..` → parent of current working directory
- `.` → current working directory
- `%VAR%` → environment variables from `shell.parms`

```python
shell.parms["MY_PATH"] = "/custom/path"
shell.file("%MY_PATH%/file.txt")  # Automatically expanded
```

### UniShell Methods

#### Creating File Objects

- **`file(path, encoding=None)`** → `File`
  - Creates File object with automatic path expansion
  - If `encoding` not specified, uses `default_encoding` or auto-detection (if enabled)

- **`files(*files, encoding=None, sep="\n")`** → `Files`
  - Creates Files object for working with multiple files
  - `sep` — separator when combining content

#### File Operations

- **`mkfile(path)` / `touch(path)`** — create empty file
- **`rmfile(path)`** — delete file
- **`nano(path, edit_txt="notepad")`** — open file in text editor
- **`recode(file_path, to_encoding, from_encoding=None)`** — re-encode file

#### Directory Operations

- **`mkdir(path, mode=0o777, parents=False, exist_ok=False)`** — create directory
- **`rmdir(path)`** — delete directory (recursively)
- **`ls(path=".", details=False)`** — list files and directories
  - If `details=True`, returns dictionary with metadata

#### File and Directory Operations

- **`copy(from_path, to_path, follow_symlinks=True)`** — copy
- **`remove(path)` / `rm(path)`** — delete file or directory
- **`make(path, is_file=None)`** — create full path (all parent directories)
- **`chmod(path, mode)`** — change access permissions

#### Archive Operations

- **`make_archive(from_path, to_path=None, format="zip")`** / **`mkarch()`** / **`mk_archive()`**
  - Create archive from file or directory
  - If `to_path` not specified, created next to source

- **`extract_archive(archive_path, extract_dir=None, format=None)`** / **`unparch()`** / **`extarch()`**
  - Extract archive
  - If `extract_dir` not specified, extracts to current directory

#### Path Operations

- **`cd(path)`** — change current working directory
- **`to_abspath(path)`** — convert path to absolute with variable expansion

#### Environment Variables (`shell.parms`)

- **`parms["VAR"] = value`** — set local variable
- **`parms.sets({"VAR1": val1, "VAR2": val2})`** — set multiple variables
- **`parms.set_gl("VAR") = value`** — set global variable
- **`parms.del("VAR")`** — delete variable
- **`parms.all()`** — list all variables

All UniShell methods return `self` for method chaining and have `ignore_errors=False` parameter.

### UniShell Method Aliases

- `touch` = `mkfile`
- `rm` = `remove`
- `rmtree` = `rmdir`
- `mkarch` / `mk_archive` = `make_archive`
- `unparch` / `unp_arch` / `extarch` / `extarch` / `unpack_archive` = `extract_archive`
- `convert_encoding` = `recode`

## Structures API

### File Class

Class for working with a single file.

#### Initialization

```python
file = File(path, encoding=None)
# path can be: str, Path, or another File object
```

#### Properties

- **`content`** (str) — file content (read/write/delete)
  - On read, automatically detects encoding on error
  - On write, automatically selects minimal suitable encoding
  - `del file.content` — clear content

- **`path`** (Path) — file path
- **`encoding`** (str) — file encoding
- **`name`** (str) — file name
- **`extension`** (str) — file extension (all suffixes)
- **`parent`** (Dir) — parent directory
- **`hidden`** (bool) — whether file is hidden

#### Methods

- **`create(mode=438, ignore_errors=True)`** — create empty file
- **`remove()`** — delete file
- **`recode(to_encoding=None, from_encoding=None)`** — re-encode
  - If `to_encoding` not specified, determines minimal suitable encoding
- **`chmod(mode)`** — change access permissions
- **`nano(edit_txt="notepad")`** — open in text editor
- **`on_disk()`** → bool — whether file exists on disk
- **`sizeof()`** → int — size in bytes
- **`created_utc()`** → datetime — creation time (UTC)
- **`modified_utc()`** → datetime — modification time (UTC)
- **`accessed_utc()`** → datetime — access time (UTC)
- **`created_lcl()`** → datetime — creation time (local)
- **`modified_lcl()`** → datetime — modification time (local)
- **`accessed_lcl()`** → datetime — access time (local)
- **`is_symlink()`** → bool — whether is symbolic link
- **`metadata()`** → dict — all file metadata

### Files Class

Class for working with multiple files.

#### Initialization

```python
files = Files(*files, encoding=None, sep="\n")
# files can be: str, Path, or File
```

#### Properties

- **`content`** (str) — combined content of all files separated by `sep`
- **`files`** (list[File]) — list of File objects
- **`sep`** (str) — separator

### Dir Class

Class for working with directories.

#### Initialization

```python
dir = Dir(path)
# path can be: str, Path, or another Dir object
```

#### Properties

- **`path`** (Path) — directory path
- **`name`** (str) — directory name (can be modified)
- **`parent`** (Dir) — parent directory (can be modified to move)
- **`hidden`** (bool) — whether directory is hidden (can be modified)

#### Methods

- **`create(mode=0o777, parents=False, ignore_errors=False)`** — create directory
- **`add(path)`** — add file or directory to directory (copy)
- **`move_to(dir)`** — move directory
- **`rename(new_name)`** — rename
- **`chmod(mode)`** — change access permissions
- **`on_disk()`** → bool — whether directory exists
- **`sizeof(recursive=True, symlink=False)`** → int — size in bytes
- **`len_files_and_dirs(recursive=True, symlinks=False)`** → dict — item count
- **`created_utc()`** → datetime — creation time (UTC)
- **`modified_utc()`** → datetime — modification time (UTC)
- **`accessed_utc()`** → datetime — access time (UTC)
- **`created_lcl()`** → datetime — creation time (local)
- **`modified_lcl()`** → datetime — modification time (local)
- **`accessed_lcl()`** → datetime — access time (local)
- **`is_symlink()`** → bool — whether is symbolic link
- **`metadata()`** → dict — all directory metadata

#### Operators

- **`dir / "filename"`** → File or Dir — access file/subdirectory
- **`for item in dir:`** — iterate over contents (returns File or Dir)

### Archive Class

Universal interface for working with archives.

#### Supported Formats

- **zip** — create, add, extract (with passwords via pyzipper)
- **7z** — create, add, extract (with passwords)
- **tar** — create, add, extract
- **tar.gz / tgz** — create, add, extract
- **tar.bz2 / tbz2** — create, add, extract
- **gz** — read and extract only (single file)
- **bz2** — read and extract only (single file)
- **rar** — read and extract only (with passwords, requires rarfile)

#### Initialization

```python
archive = Archive(path, format=None, password=None)
# format is automatically determined by extension if not specified
```

#### Methods

- **`add(path, arcname=None)`** — add file or directory to archive
- **`extract(path, member=None)`** — extract archive or specific member
- **`list_files()`** → list[str] — list files in archive
- **`create()`** — create empty archive
- **`cleanup()`** — remove temporary files (for 7z and tar)

#### Class Methods

- **`Archive.create_from(path, format, files, password=None)`** — create archive with files

#### Iteration

```python
for filename in archive:
    print(filename)  # File names in archive
```

## Stream Operators (>>, >, <<, <)

`File` and `Files` classes support operators for content manipulation:

- **`a > b`** — copies content from `a` to `b` (overwrites `b`)
- **`a >> b`** — appends content from `a` to end of `b` (respects `sep`)
- **`a < b`** — copies content from `b` to `a` (overwrites `a`)
- **`a << b`** — appends content from `b` to end of `a` (respects `sep`)

```python
from FileAlchemy.structures import File, Files

file1 = File("a.txt")
file2 = File("b.txt")
file1 > file2  # Copies content from a.txt to b.txt

files = Files("1.txt", "2.txt")
combined = File("combined.txt")
files >> combined  # Appends content from all files to combined.txt
```

## Usage Examples

### Example 1: Backup (UniShell)

```python
from FileAlchemy import UniShell
import datetime

shell = UniShell()
today = datetime.datetime.now().strftime("%Y-%m-%d")
shell.make_archive("project", f"backups/project_{today}.zip")
```

### Example 2: Logging (Structures)

```python
from FileAlchemy.structures import File
import datetime

log_file = File("app.log")
log_entry = f"{datetime.datetime.now()}: New event\n"
log_file.content = log_file.content + log_entry
```

### Example 3: Working with Config Files (UniShell)

```python
from FileAlchemy import UniShell
import json

shell = UniShell()
config = shell.file("config.json").content
settings = json.loads(config)
settings["timeout"] = 30
shell.file("config.json").content = json.dumps(settings, indent=2)
```

### Example 4: Processing Multiple Files (Structures)

```python
from FileAlchemy.structures import Files, File

files = Files("file1.txt", "file2.txt", "file3.txt", sep="\n---\n")
all_content = files.content  # Combined content
File("combined.txt").content = all_content
```

### Example 5: Working with Archives (Structures)

```python
from FileAlchemy.structures import Archive

# Create archive
archive = Archive("backup.zip")
archive.add("file1.txt")
archive.add("directory/")

# Extract
archive.extract("extracted/")

# List files
print(archive.list_files())
```

## Windows-Specific Features

The `FileAlchemy.Windows.regedit` module provides Windows registry and user account management (requires `pywin32`):

```python
from FileAlchemy.Windows.regedit import CurrentUser, User, Users, PATH, AutoRun

# Current user
cur_user = CurrentUser()
print(cur_user.PATH.all())  # Current user's PATH

# Working with PATH
cur_user.PATH.add("C:/new/path")
cur_user.PATH.pop("C:/old/path")

# AutoRun
cur_user.AutoRun.add("MyApp", "C:/app.exe")
cur_user.AutoRun.remove("MyApp")

# Working with users
user = User(name="username")
users = Users.local()  # List of local users
```

## Implementation Features

1. **Lazy operations** — files are read only when needed
2. **Auto-recovery** — automatic encoding detection on read errors
3. **Safety** — file existence checks before operations
4. **Cross-platform** — unified API for Windows, Linux, and macOS
5. **Two-level API** — shell-style (UniShell) and Python-style (structures)
6. **Stream operations** — support for >>, >, <<, < operators for content manipulation

## License

FileAlchemy is distributed under the **MIT License**. See LICENSE file for details.

### Dependency Licenses

The project uses the following dependencies with their licenses:

- **chardet** — LGPL
- **py7zr** — LGPL-2.1-or-later
- **pyzipper** — MIT
- **rarfile** — ISC
- **pywin32** (optional) — PSF (Python Software Foundation License)

All dependencies are compatible with MIT License. For detailed information, see [LICENSES_DEPENDENCIES.md](LICENSES_DEPENDENCIES.md).

## Author

GimpNiK (https://github.com/GimpNiK) — Developer and maintainer of the project.
