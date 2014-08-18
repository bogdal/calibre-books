import os

from django.conf import settings
from calibre_books.core.utils import DropboxStorage
from PIL import Image

from .models import Book


def synchronize_calibre():
    storage = DropboxStorage()

    storage.sync_db()

    for book in Book.objects.all():

        dropbox_cover_path = '/%s/%s/cover.jpg' % (settings.DROPBOX_CALIBRE_DIR, book.path)
        cover_path = "%s/cover-%s.jpg" % (settings.MEDIA_ROOT, book.uuid)
        thumb_path = "%s/%s.jpg" % (settings.MEDIA_ROOT, book.uuid)

        if not os.path.exists(thumb_path):
            cover = storage.get_file(dropbox_cover_path)
            if cover:
                with open(cover_path, 'wb') as f:
                    f.write(cover.read())

                cover_width = 300
                img = Image.open(cover_path)
                width_percent = (cover_width/float(img.size[0]))
                cover_height = int((float(img.size[1]) * float(width_percent)))
                img = img.resize((cover_width, cover_height), Image.ANTIALIAS)
                img.save(thumb_path)

                os.remove(cover_path)
