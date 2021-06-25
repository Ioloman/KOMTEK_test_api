sleep "20s"
pipenv run -v python manage.py migrate
pipenv run -v python manage.py runserver 0.0.0.0:8000