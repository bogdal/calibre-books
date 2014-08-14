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
        'django-dropbox==0.0.2',
        'dj_database_url>=0.2.2',
        'python-memcached==1.53',
        'PIL==1.1.7',
        'gunicorn==19.1.0',
        'psycopg2==2.5.3',

    ],
    entry_points={
        'console_scripts': ['manage.py = calibre_books:manage']},
)
