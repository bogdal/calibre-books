from django.conf import settings
from django.db import models
from calibre_books.core.utils import get_dropbox_url


class Author(models.Model):

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'authors'


class Book(models.Model):

    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=255)
    sort = models.CharField(max_length=255)
    timestamp = models.DateTimeField(max_length=255)
    pubdate = models.DateTimeField(max_length=255)
    path = models.CharField(max_length=255)
    uuid = models.CharField(max_length=255)
    last_modified = models.DateTimeField(max_length=255)
    authors = models.ManyToManyField(Author, through='AuthorBook')

    def __unicode__(self):
        return self.title

    def _get_extra_value(self, name):
        try:
            data = self.plugin_data.get(name=name)
        except PluginData.DoesNotExist:
            pass
        else:
            return data.value

    @property
    def cover_url(self):
        return self._get_extra_value('cover_url')

    def set_data(self, name, value):
        data, _ = self.plugin_data.get_or_create(name=name)
        data.value = value
        data.save()

    class Meta:
        db_table = 'books'
        ordering = ('last_modified',)


class AuthorBook(models.Model):

    book = models.ForeignKey(Book, db_column='book')
    author = models.ForeignKey(Author, db_column='author')

    class Meta:
        db_table = 'books_authors_link'


class Data(models.Model):

    PDF = 'PDF'
    MOBI = 'MOBI'
    EPUB = 'EPUB'

    FORMATS = (
        (PDF, "Pdf"),
        (MOBI, 'Mobi'),
        (EPUB, 'Epub')
    )

    book = models.ForeignKey(Book, db_column='book', related_name='data')
    format = models.CharField(max_length=255, choices=FORMATS)
    size = models.IntegerField(db_column='uncompressed_size')
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'data'
        ordering = ('format',)

    @property
    def download_url(self):
        path = '/%s/%s/%s.%s' % (settings.DROPBOX_CALIBRE_DIR, self.book.path, self.name, self.format.lower())
        return get_dropbox_url(path)


class PluginData(models.Model):

    book = models.ForeignKey(Book, db_column='book', related_name='plugin_data')
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255, db_column='val')

    class Meta:
        db_table = 'books_plugin_data'
