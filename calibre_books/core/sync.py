import os

from django.conf import settings
from django.core.management import call_command
from calibre_books.calibre.models import Book

from .utils import DropboxStorage


def synchronize_calibre(force_update=False):
    storage = DropboxStorage()

    if force_update or storage.need_update():
        storage.sync_db()

        for book in Book.objects.all():
            cover_path = ('/%s/%s/cover.jpg' % (
                settings.DROPBOX_CALIBRE_DIR, book.path))
            thumb_path = "%s/%s.jpg" % (settings.MEDIA_ROOT, book.uuid)

            if not os.path.exists(thumb_path):
                cover = storage.client.thumbnail(cover_path)
                if cover:
                    with open(thumb_path, 'wb') as f:
                        f.write(cover.read())

        # search indexes
        call_command("update_index")
