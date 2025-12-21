# Лицензии зависимостей FileAlchemy

FileAlchemy распространяется под лицензией **MIT License**. Ниже перечислены лицензии всех зависимостей проекта.

## Основные зависимости

| Пакет | Лицензия | Совместимость с MIT |
|-------|----------|---------------------|
| **chardet** | LGPL | ✅ Да (при использовании как библиотеки) |
| **py7zr** | LGPL-2.1-or-later | ✅ Да (при использовании как библиотеки) |
| **pyzipper** | MIT | ✅ Да |
| **rarfile** | ISC | ✅ Да |

## Опциональные зависимости (Windows)

| Пакет | Лицензия | Совместимость с MIT |
|-------|----------|---------------------|
| **pywin32** | PSF (Python Software Foundation License) | ✅ Да |

## Примечания о лицензиях

### LGPL (GNU Lesser General Public License)
- **chardet** и **py7zr** используют LGPL
- LGPL совместима с MIT при использовании библиотек как динамически подключаемых модулей
- При распространении FileAlchemy необходимо сохранять информацию о лицензиях этих зависимостей

### ISC License
- **rarfile** использует ISC License
- ISC License очень похожа на MIT и полностью совместима

### PSF License
- **pywin32** использует Python Software Foundation License
- PSF License совместима с MIT

## Совместимость

Все зависимости FileAlchemy совместимы с MIT License. Проект может свободно распространяться под лицензией MIT.

## Дополнительная информация

Для получения полной информации о лицензиях зависимостей используйте:

```bash
pip show chardet py7zr pyzipper rarfile pywin32
```

Или посетите страницы пакетов на PyPI:
- [chardet](https://pypi.org/project/chardet/)
- [py7zr](https://pypi.org/project/py7zr/)
- [pyzipper](https://pypi.org/project/pyzipper/)
- [rarfile](https://pypi.org/project/rarfile/)
- [pywin32](https://pypi.org/project/pywin32/)

