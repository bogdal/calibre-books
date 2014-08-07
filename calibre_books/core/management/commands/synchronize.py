from django.core.management.base import NoArgsCommand
from django.conf import settings
from django_dropbox.storage import DropboxStorage
from dropbox.rest import ErrorResponse

from calibre_books.calibre.models import Book


class Command(NoArgsCommand):

    def handle_noargs(self, **options):

        client = DropboxStorage().client
        for book in Book.objects.all():

            try:
                url = client.media('/%s/%s/cover.jpg' % (settings.DROPBOX_CALIBRE_DIR, book.path)).get('url')
            except ErrorResponse:
                pass
            else:
                data, _ = book.plugin_data.get_or_create(name='cover_url')
                data.value = url
                data.save()
