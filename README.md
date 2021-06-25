Запуск через Docker с postgres:

`docker-compose up -d`

Запуск вручную с sqlite через pipenv:

```
pip install pipenv
pipenv install
pipenv run python manage.py migrate
pipenv run python manage.py runserver
```