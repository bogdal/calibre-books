from unittest import TestSuite, TestLoader

import django


if hasattr(django, 'setup'):
    django.setup()

TEST_MODULES = [
    'calibre_books.calibre.tests',
]

suite = TestSuite()
loader = TestLoader()
for module in TEST_MODULES:
    suite.addTests(loader.loadTestsFromName(module))
