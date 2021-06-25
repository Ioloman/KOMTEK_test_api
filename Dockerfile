FROM python:3.9.5

WORKDIR /usr/src/KOMTEK

COPY . .
COPY ./entrypoint.sh /run/entrypoint.sh

RUN apt update
RUN apt install -y python3-dev libpq-dev
RUN pip install pipenv
RUN pipenv install
RUN pipenv install psycopg2
RUN pipenv run -v python manage.py makemigrations

EXPOSE 8000

ENTRYPOINT /run/entrypoint.sh