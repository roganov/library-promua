## Local installation
First we need to install the environment and required packages
```sh
$ virtualenv .evn  # or wherever you want the venv to be placed
$ pip install -r requirements/local.txt
$ source .env/bin/activate  # activate your virtual env
```
The database (sqlite is used for development) can be set up either way:
1. via migrations: `python manage.py db upgrade`
2. or using the provided schema.sql script: `sqlite3 db.sqlite < schema.sql`

The first approach is generally preferred.

## Loading initial data
```sh
$ sqlite3 db.sqlite < initialdata.sql
```
There are two users provided:
- email: user@mail.com password: 222222 -- no privileges
- email: superuser@mail.com password 111111 -- superuser, can add and edit books/authors

## Running develompent webserver
```sh
$ python run.py
```

## Running tests
```sh
$ FLASK_CONFIG=config.TestConfig nosetests -v
```