import os
from django.core.management.base import NoArgsCommand
from django.conf import settings
from django_dropbox.storage import DropboxStorage
from dropbox.rest import ErrorResponse
from PIL import Image

from calibre_books.calibre.models import Book


class Command(NoArgsCommand):

    def handle_noargs(self, **options):

        client = DropboxStorage().client
        calibre_db_path = '/%s/metadata.db' % settings.DROPBOX_CALIBRE_DIR
        calibre_db = client.get_file(calibre_db_path)

        with open(settings.DATABASES['calibre']['NAME'], 'wb') as f:
            f.write(calibre_db.read())

        for book in Book.objects.all():
            print book.title,

            dropbox_cover_path = '/%s/%s/cover.jpg' % (settings.DROPBOX_CALIBRE_DIR, book.path)
            cover_path = "%s/cover-%s.jpg" % (settings.MEDIA_ROOT, book.uuid)
            thumb_path = "%s/%s.jpg" % (settings.MEDIA_ROOT, book.uuid)

            if not os.path.exists(thumb_path):
                try:
                    cover = client.get_file(dropbox_cover_path)
                except ErrorResponse:
                    pass
                else:
                    with open(cover_path, 'wb') as f:
                        f.write(cover.read())

                    cover_width = 300
                    img = Image.open(cover_path)
                    width_percent = (cover_width/float(img.size[0]))
                    cover_height = int((float(img.size[1]) * float(width_percent)))
                    img = img.resize((cover_width, cover_height), Image.ANTIALIAS)
                    img.save(thumb_path)

                    os.remove(cover_path)
            print 'done'
