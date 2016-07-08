#!/bin/sh
python manage.py synchronize
python manage.py collectstatic --noinput
uwsgi /app/calibre_books/wsgi/uwsgi.ini
