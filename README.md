# Продуктовый помощник.

Рецепты и списки покупок.

![Action status](https://github.com/Nastasia153/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)


## Установка

Клонируйте репозиторий.

## Использование

Наполнение .env файла.

В директории backend, есть шаблон .env.example по заполнению файла

## Запуск docker-compose

```bash
sudo docker-compose up -d
```
- выполняем миграции:

```bash
sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate
```
- заполняем базу ингредиентами и тегами:

```bash
sudo docker-compose exec web python manage.py sampledata
```

- cоздаём суперпользователя:

```bash
sudo docker-compose exec web python manage.py createsuperuser
```
- собираем статику:
```bash
sudo docker-compose exec web python manage.py collectstatic --no-input
```


## Использование

Теперь проект доступен по адресу:
[http://coocwithme.ddns.net/](http://coocwithme.ddns.net/)

документация API доступна по адресу 
[http://coocwithme.ddns.net/api/docs/redoc](http://coocwithme.ddns.net/api/docs/redoc)

## Данные для администратора
email - admin@ya.ru

password - fl789vby

## Teхнологии
Приложение работает на 
- [Django 2.2](https://www.djangoproject.com/download/)
- [Django REST Framework 3.12](https://www.django-rest-framework.org/#installation).
- [Djoser](https://djoser.readthedocs.io/en/latest/getting_started.html)
- [Docker](https://docs.docker.com/)
- [GitHub Actions](https://github.com/features/actions)


## Разработчики

- [Анастасия Дементьева](https://github.com/Nastasia153)

