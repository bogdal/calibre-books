#! /usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calibre_books.settings')

setup(
    name='calibre-books',
    author='Adam Bogdał',
    author_email='adam@bogdal.pl',
    description="Calibre server in Django",
    license='BSD',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=1.6',
        'django-bootstrap3>=4.8.2',
        'dropbox==2.1.0',
        'dj_database_url>=0.2.2',
        'Pillow==2.5.2',
        'gunicorn==19.1.0',
        'psycopg2==2.5.3',
        'dj-static==0.0.6',
        'django-sslify==0.2.3',
        'raven==5.0.0',
        'python-memcached==1.53',
        'django-haystack==2.2.0',
        'whoosh==2.6.0',
        'django-debug-toolbar>=1.2.1',
    ],
    entry_points={
        'console_scripts': ['manage.py = calibre_books:manage']},
)
