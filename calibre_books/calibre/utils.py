import collections
from django.conf import settings
from django.db import models


def create_model(name, fields=None, module='', options=None):
    class Meta:
        pass

    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    attrs = {'__module__': module, 'Meta': Meta}

    if fields:
        attrs.update(fields)

    return type(name, (models.Model,), attrs)


def get_user_bookshelf(user):
    bookshelves = [u.split(':') for u in settings.BOOKSHELVES_USERS]
    for bookshelf, address in bookshelves:
        if '@' in address and user.email.endswith(address):
            return bookshelf
    return settings.DEFAULT_BOOKSHELF


def get_genres_as_tree(genres, tree=None):
    tree = tree or {}
    for genre in genres:
        leaves = genre.split('.')
        if len(leaves):
            main = leaves.pop(0)
            tree.setdefault(main, {})
            if len(leaves):
                tree[main] = (get_genres_as_tree(
                    ['.'.join(leaves)], tree[main]))
    return collections.OrderedDict(sorted(tree.iteritems()))
