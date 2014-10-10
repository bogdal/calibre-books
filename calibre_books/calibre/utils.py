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
