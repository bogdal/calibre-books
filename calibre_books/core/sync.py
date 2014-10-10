import os

from django.conf import settings
from django.core.management import call_command
from calibre_books.calibre.models import Book
from PIL import Image

from .utils import DropboxStorage


def synchronize_calibre(force_update=False):
    storage = DropboxStorage()

    if force_update or storage.need_update():
        storage.sync_db()

        for book in Book.objects.all():

            dropbox_cover_path = ('/%s/%s/cover.jpg' %
                                  (settings.DROPBOX_CALIBRE_DIR, book.path))
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
                    cover_height = int((float(img.size[1]) *
                                        float(width_percent)))
                    img = img.resize((cover_width, cover_height),
                                     Image.ANTIALIAS)
                    img.save(thumb_path)

                    os.remove(cover_path)

        # search indexes
        call_command("update_index")
