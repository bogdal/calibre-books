#! /usr/bin/env python
from setuptools import setup, find_packages, Command
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
    ],
    entry_points={
        'console_scripts': ['manage.py = calibre_books:manage']},
    )

