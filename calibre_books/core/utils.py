from django.conf import settings
from django.core.cache import cache
from dropbox.client import DropboxClient
from dropbox.rest import ErrorResponse
from dropbox.session import DropboxSession


class DropboxStorage(object):

    calibre_db_path = '/%s/metadata.db' % settings.DROPBOX_CALIBRE_DIR
    dropbox_cursor_key = 'dropbox_cursor'

    def __init__(self):
        session = DropboxSession(settings.DROPBOX_CONSUMER_KEY, settings.DROPBOX_CONSUMER_SECRET,
                                 settings.DROPBOX_ACCESS_TYPE, locale=None)
        session.set_token(settings.DROPBOX_ACCESS_TOKEN, settings.DROPBOX_ACCESS_TOKEN_SECRET)
        self.client = DropboxClient(session)

    def get_url(self, path, share=False):
        try:
            if share:
                return self.client.share(path, short_url=False)['url'] + '?dl=1'
            return self.client.media(path).get('url')
        except ErrorResponse:
            pass

    def get_file(self, path):
        try:
            return self.client.get_file(path)
        except ErrorResponse:
            pass

    def sync_db(self):
        calibre_db = self.client.get_file(self.calibre_db_path)

        with open(settings.DATABASES['calibre']['NAME'], 'wb') as f:
            f.write(calibre_db.read())

    def need_update(self):
        delta = self.client.delta(cursor=cache.get(self.dropbox_cursor_key), path_prefix=self.calibre_db_path)
        cache.set(self.dropbox_cursor_key, delta['cursor'], timeout=None)
        return len(delta['entries']) > 0
