from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.utils import override_settings

from .utils import get_user_bookshelf


class BookshelfTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.admin1 = User(email='admin1@admin.com')
        self.admin2 = User(email='admin2@admin.com')
        self.admin3 = User(email='admin3@admin.com')
        self.user1 = User(email='test1@example.com')
        self.user2 = User(email='test2@example.com')

    @override_settings(DEFAULT_BOOKSHELF='default', BOOKSHELVES_USERS=[
        'test:admin1@admin.com', ':@admin.com', 'read:test1@example.com'])
    def test_bookshelves(self):

        expected_bookshelves = ['test', '', '', 'read', 'default']

        bookshelves = [
            get_user_bookshelf(self.admin1),
            get_user_bookshelf(self.admin2),
            get_user_bookshelf(self.admin3),
            get_user_bookshelf(self.user1),
            get_user_bookshelf(self.user2)]

        self.assertEqual(bookshelves, expected_bookshelves)
