from django.core.management.base import NoArgsCommand
from django.conf import settings
from django_dropbox.storage import DropboxStorage

from calibre_books.calibre.models import Book
from calibre_books.core.utils import get_dropbox_url


class Command(NoArgsCommand):

    def handle_noargs(self, **options):

        client = DropboxStorage().client
        calibre_db_path = '/%s/metadata.db' % settings.DROPBOX_CALIBRE_DIR
        calibre_db = client.get_file(calibre_db_path)

        local_db = open(settings.DATABASES['calibre']['NAME'], 'wb')
        local_db.write(calibre_db.read())
        local_db.close()

        for book in Book.objects.all():
            print book.title,
            if not book.cover_url:
                cover_path = '/%s/%s/cover.jpg' % (settings.DROPBOX_CALIBRE_DIR, book.path)
                book.cover_url = get_dropbox_url(cover_path, share=True)
            print 'done'
