from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import NoArgsCommand
from django.conf import settings
from django_dropbox.storage import DropboxStorage
from dropbox.rest import ErrorResponse

from calibre_books.calibre.models import Book, Data


class Command(NoArgsCommand):

    def get_url(self, path):
        try:
            return self.client.media(path).get('url')
        except ErrorResponse:
            pass

    def handle_noargs(self, **options):

        self.client = DropboxStorage().client

        for book in Book.objects.all():
            print book.title,

            url = self.get_url('/%s/%s/cover.jpg' % (settings.DROPBOX_CALIBRE_DIR, book.path))
            if url:
                book.set_data('cover_url', url)

            try:
                data = book.data.get(format=Data.MOBI)
            except ObjectDoesNotExist:
                pass
            else:
                url = self.get_url('/%s/%s/%s.mobi' % (settings.DROPBOX_CALIBRE_DIR, book.path, data.name))
                if url:
                    book.set_data('download_url', url)
            print 'done'
