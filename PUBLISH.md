# Инструкция по публикации на PyPI

## Подготовка

1. Убедитесь, что у вас установлены необходимые инструменты:
```bash
pip install build twine
```

2. Проверьте, что все файлы на месте:
   - `pyproject.toml` - конфигурация проекта
   - `setup.py` - для обратной совместимости
   - `MANIFEST.in` - список дополнительных файлов
   - `README.md` - описание на английском
   - `LICENSE` - лицензия

## Сборка пакета

1. Очистите старые сборки (если есть):
```bash
rm -rf dist/ build/ *.egg-info
```

2. Соберите пакет:
```bash
python -m build
```

Это создаст:
- `dist/FileAlchemy-1.1.1.tar.gz` - исходный дистрибутив
- `dist/FileAlchemy-1.1.1-py3-none-any.whl` - wheel дистрибутив

## Проверка перед публикацией

1. Проверьте содержимое архива:
```bash
tar -tzf dist/FileAlchemy-1.1.1.tar.gz
```

2. Проверьте метаданные:
```bash
python -m twine check dist/*
```

3. Протестируйте установку локально:
```bash
pip install dist/FileAlchemy-1.1.1-py3-none-any.whl
```

## Публикация на TestPyPI (рекомендуется сначала)

1. Зарегистрируйтесь на https://test.pypi.org/account/register/

2. Загрузите на TestPyPI:
```bash
python -m twine upload --repository testpypi dist/*
```

3. Протестируйте установку с TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ FileAlchemy
```

## Публикация на PyPI

1. Зарегистрируйтесь на https://pypi.org/account/register/ (если еще не зарегистрированы)

2. Создайте API токен на https://pypi.org/manage/account/token/

3. Загрузите на PyPI:
```bash
python -m twine upload dist/*
```

Или с указанием учетных данных:
```bash
python -m twine upload dist/* --username __token__ --password <ваш_токен>
```

## Обновление версии

При обновлении версии:

1. Измените версию в:
   - `pyproject.toml` (version = "X.X.X")
   - `setup.py` (version="X.X.X")
   - `FileAlchemy/__init__.py` (__version__ = "X.X.X")
   - `README.md` и `README.ru.md` (если нужно)

2. Соберите и опубликуйте заново:
```bash
python -m build
python -m twine upload dist/*
```

## Полезные команды

- Просмотр информации о пакете: `pip show FileAlchemy`
- Удаление пакета: `pip uninstall FileAlchemy`
- Установка конкретной версии: `pip install FileAlchemy==1.1.1`

## Примечания

- После публикации на PyPI пакет будет доступен через `pip install FileAlchemy`
- Версии нельзя перезаписывать - каждая версия должна быть уникальной
- Для Windows-специфичных функций используйте: `pip install FileAlchemy[windows]`

