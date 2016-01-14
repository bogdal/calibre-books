#! /usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calibre_books.test_settings')

with open('requirements.txt', 'r') as req_file:
    requirements = req_file.readlines()

setup(
    name='calibre-books',
    author='Adam Bogdał',
    author_email='adam@bogdal.pl',
    description="Calibre server in Django",
    license='BSD',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    test_suite='calibre_books.tests.suite',
    entry_points={
        'console_scripts': ['calibre_books = calibre_books:manage']},
)
