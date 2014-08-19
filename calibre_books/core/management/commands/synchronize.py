from django.core.management.base import NoArgsCommand
from calibre_books.core.sync import synchronize_calibre


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        synchronize_calibre(force_update=True)
