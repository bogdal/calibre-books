from django.conf import settings
from django.core.cache import cache
from django.db import models
from django_dropbox.storage import DropboxStorage
from dropbox.rest import ErrorResponse


class Book(models.Model):

    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=255)
    sort = models.CharField(max_length=255)
    timestamp = models.DateTimeField(max_length=255)
    pubdate = models.DateTimeField(max_length=255)
    path = models.CharField(max_length=255)
    uuid = models.CharField(max_length=255)
    last_modified = models.DateTimeField(max_length=255)

    @property
    def cover_url(self):
        cache_key = 'cover-url-%s' % self.uuid
        url = cache.get(cache_key)
        if not url:
            client = DropboxStorage().client
            try:
                url = client.media('/%s/%s/cover.jpg' % (settings.DROPBOX_CALIBRE_DIR, self.path)).get('url')
            except ErrorResponse:
                url = ''
            else:
                cache.set(cache_key, url)
        return url

    class Meta:
        db_table = 'books'
