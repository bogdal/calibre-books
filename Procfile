web: python manage.py migrate --noinput &&  python manage.py synchronize && python manage.py collectstatic --noinput && gunicorn calibre_books.wsgi
