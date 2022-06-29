# praktikum_new_diplom
## Установка

Клонируйте репозиторий.

Создайте и активируйте виртуальное окружение:

В Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

В Windows
```bash
python -m venv venv
source venv/Scripts/activate
```

Используйте [pip](https://pip.pypa.io/en/stable/)
для установки зависимостей.

```bash
pip install -r requirements.txt
```

Создайте базу данных

```bash
python backend/manage.py migrate
```

Создайте суперпользователя

```bash
python backend/manage.py createsuperuser
```


## Тестовый набор данных

Тестовый набор данных можно загрузить, используя команду

```bash
python backend/manage.py sampledata
```

## Использование

Проверка установки

```bash
python backend/manage.py runserver
```
после запуска локального сервера, данные доступны по адресу [http://127.0.0.1:8000/api](http://127.0.0.1:8000/api)