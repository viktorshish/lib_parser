# lib_parser
Парсер онлайн библиотеки.

Скачивает книги с сайта [tululu.org](https://tululu.org).

## Как запустить

Для изоляции проекта рекомендуется развернуть виртуальное окружение:

для Linux и MacOS
```bash
python3 -m venv env
source env/bin/activate
```

для Windows
```bash
python -m venv env
venv\Scripts\activate.bat
```

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

```bash
pip install -r requirements.txt
```

## Использование

Для запуска скрипта:

```bash
python tululu.py START_ID COUNT
```
где: 
    
**START_ID** - ID книги (число), с которой начнется скачивание книг

**COUNT** - Количество скачиваемых книг
