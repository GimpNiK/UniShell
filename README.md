# FileAlchemy

**FileAlchemy v. 1.1.1** — A powerful and intuitive Python library for working with files, directories, and text data. It provides a convenient interface for performing file system operations, text processing, and encoding management, inspired by Unix and Cmd command-line syntax. Most command names duplicate functionality from these two command shells. Designed to be used instead of bat and sh files, and in interactive mode in Python Shell.

## Main Modules

1. **UniShell (main class)** — High-level interface for working with files and directories
   - File, directory, and archive management
   - Encoding operations
   - Operator overloading for convenient content manipulation

2. **structures** — Low-level classes for file system operations
   - `File` — Class for working with a single file
   - `Files` — Class for working with a group of files
   - `Dir` — Class for working with directories
   - `Archive` — Universal class for working with archives (zip, 7z, tar, rar, etc.)
   - `Stream` — Base class for stream operations

3. **Encodings** — Automatic detection and re-encoding of files

4. **Windows Registry and User Accounts** (Windows only)
   - Create, view, delete user accounts
   - Edit and view PATH, Run, RunOnce

## Key Features

1. **File and Directory Management**:
   - Create, copy, delete, write text
   - Archive support: zip, 7z, tar, tar.gz, tar.bz2, rar, gz, bz2
   - Access rights management (chmod)
   - File metadata retrieval (size, creation/modification dates, hidden status, etc.)

2. **Text Processing**:
   - Read and write files with automatic encoding detection
   - Re-encoding between different encodings
   - In-memory text operations

3. **Convenient Interface**:
   - Method chaining
   - Operator overloading >, >>, <, << for file content operations
   - Support for special paths (~, .., environment variables)

4. **Cross-platform**:
   - Works on Windows, Linux, and macOS
   - Unified API for different operating systems

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
- Dependencies:
  - `chardet` (for automatic encoding detection)
  - For archive support: `py7zr`, `rarfile` (optional)
  - For Windows functions: `pywin32` (optional, install with `[windows]` extra)

## Quick Start

### Using UniShell Class (High-level API)

```python
from FileAlchemy import UniShell

# Initialization
shell = UniShell()

# Change working directory
shell.cd("..")

# Create file and write text
shell.file("test.txt").content = "Hello, world!"

# Read file
content = shell.file("test.txt").content
print(content)  # "Hello, world!"

# Save content from multiple files into one
shell.files("1.txt", "2.txt") >> shell.file("3.txt")

# Clear file content
del shell.file("3.txt").content

# Copy file
shell.copy("test.txt", "backup.txt")

# Work with archives
shell.make_archive("backup.txt", "archive.zip")
```

### Using structures Module (Low-level API)

```python
from FileAlchemy.structures import File, Files, Dir, Archive

# Work with file
file = File("test.txt")
file.content = "Hello, world!"
print(file.content)

# Work with group of files
files = Files("1.txt", "2.txt", "3.txt")
combined_content = files.content  # Combined content

# Work with directory
dir = Dir("my_folder")
dir.create()
for item in dir:  # Iterate over files and folders
    print(item)

# Work with archives
archive = Archive("data.zip")
archive.extract("extracted/")
archive.add_file("new_file.txt")
```

## Operator Overloading

The library provides convenient operators for working with content:

```python
# Overwrite content
shell.file("a.txt") > shell.file("b.txt")  # a.txt → b.txt
shell.file("b.txt") < shell.file("a.txt")  # b.txt ← a.txt

# Append content
shell.file("1and2.txt") << shell.files("1.txt", "2.txt")
```

## Encoding Management

The library automatically detects file encodings and provides methods for working with them:

```python
# Automatic encoding detection
file_obj = shell.file("unknown.txt")
print(file_obj.encoding)  # e.g., "utf-8" or "cp1251"

# Re-encode file
file_obj.recode("utf-8")

# Determine minimal suitable encoding
from FileAlchemy.encoding_utils import determine_minimal_encoding
min_encoding = determine_minimal_encoding("Text")
```

## Examples

### 1. Creating Backups

```python
import datetime
from FileAlchemy import UniShell

shell = UniShell()
today = datetime.datetime.now().strftime("%Y-%m-%d")
shell.make_archive("project", f"backups/project_{today}.zip")
```

### 2. Logging

```python
from FileAlchemy import UniShell

shell = UniShell()
# Add entry to log file
log_entry = f"{datetime.datetime.now()}: New event\n"
log_file = shell.file("app.log")
log_file.content = log_file.content + log_entry
```

### 3. Working with Configuration Files

```python
from FileAlchemy import UniShell
import json

shell = UniShell()
# Read config
config = shell.file("config.json").content
settings = json.loads(config)

# Modify and save
settings["timeout"] = 30
shell.file("config.json").content = json.dumps(settings, indent=2)
```

## Implementation Features

1. **Lazy operations** - Files are read only when needed
2. **Auto-recovery** - Automatic encoding detection on read errors
3. **Safety** - File existence checks before operations
4. **Cross-platform** - Unified API for different operating systems
5. **Two-level API** - High-level (UniShell) and low-level (structures)
6. **Stream operations** - Support for >>, >, <<, < operators for content manipulation

## License

MIT License. See LICENSE file for details.

## Author

GimpNiK (https://github.com/GimpNiK) - Developer and maintainer of the project.

