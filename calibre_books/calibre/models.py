from django.conf import settings
from django.db import models, OperationalError
from calibre_books.core.utils import DropboxStorage

from .utils import create_model, get_user_bookshelf, get_genres_as_tree

GENRE_TAG = 'genre'


class Author(models.Model):

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'authors'


class BookManager(models.Manager):

    def get_queryset(self):
        qs = super(BookManager, self).get_queryset()
        return (qs.prefetch_related('book_series', 'book_series__series',
                                    'data', 'authors')
                .exclude(publishers__name='calibre')
                .exclude(tags__name__in=['Clippings']))

    def by_column_value(self, label=None, value=None):
        relation_name = 'custom_column_%s' % label
        if not hasattr(self.model, relation_name):
            return self.none()
        kwargs = {}
        if label:
            kwargs['%s__value' % relation_name] = value
        return self.filter(**kwargs)

    def for_user(self, user):
        bookshelf = get_user_bookshelf(user)
        if not user.is_staff and bookshelf:
            return self.by_column_value(bookshelf, value=True)
        return self.filter()


class Book(models.Model):

    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=255)
    sort = models.CharField(max_length=255)
    timestamp = models.DateTimeField(max_length=255)
    pubdate = models.DateTimeField(max_length=255)
    series_index = models.FloatField(default=1.0)
    path = models.CharField(max_length=255)
    uuid = models.CharField(max_length=255)
    last_modified = models.DateTimeField(max_length=255)
    authors = models.ManyToManyField('Author', through='AuthorBook')
    publishers = models.ManyToManyField('Publisher', through='PublisherBook')
    tags = models.ManyToManyField('Tag', through='TagBook')

    objects = BookManager()

    def __unicode__(self):
        return self.title

    @property
    def series(self):
        series = self.book_series.all()
        if series:
            return series[0].series

    @property
    def cover_url(self):
        return "%s%s.jpg" % (settings.MEDIA_URL, self.uuid)

    @property
    def genres(self):
        genre_column = 'custom_column_%s' % GENRE_TAG
        if hasattr(self, genre_column):
            return getattr(self, genre_column).values_list(
                'value__value', flat=True)
        return []

    @classmethod
    def has_genres(cls):
        return CustomColumn.objects.filter(label=GENRE_TAG).exists()

    @classmethod
    def get_genres(cls, user):
        genre_column = 'custom_column_%s' % GENRE_TAG
        kwargs = {'%s__value__isnull' % genre_column: False}
        genres = set(cls.objects.for_user(user).filter(**kwargs).values_list(
            '%s__value__value' % genre_column, flat=True))
        return get_genres_as_tree(genres)

    def get_description(self):
        comments = self.comments.all()
        if comments:
            return comments[0]

    class Meta:
        db_table = 'books'
        ordering = ('-timestamp',)


class AuthorBook(models.Model):

    book = models.ForeignKey(Book, db_column='book')
    author = models.ForeignKey(Author, db_column='author')

    class Meta:
        db_table = 'books_authors_link'


class Comment(models.Model):

    book = models.ForeignKey(Book, db_column='book', related_name='comments')
    text = models.TextField()

    class Meta:
        db_table = 'comments'


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
        path = '/%s/%s/%s.%s' % (settings.DROPBOX_CALIBRE_DIR, self.book.path,
                                 self.name, self.format.lower())
        return DropboxStorage().get_url(path)


class PluginData(models.Model):

    book = models.ForeignKey(Book, db_column='book',
                             related_name='plugin_data')
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255, db_column='val')

    class Meta:
        db_table = 'books_plugin_data'


class Identifier(models.Model):

    urls = {
        'amazon': 'http://amzn.com/%s',
        'google': 'http://books.google.com/books?id=%s',
        'goodreads': 'https://www.goodreads.com/book/show/%s',
        'isbn': 'http://www.worldcat.org/isbn/%s'}

    book = models.ForeignKey(Book, db_column='book',
                             related_name='identifiers')
    type = models.CharField(max_length=255)
    value = models.CharField(max_length=255, db_column='val')

    class Meta:
        db_table = 'identifiers'

    def get_url(self):
        if self.type in self.urls:
            return self.urls[self.type] % self.value


class Publisher(models.Model):

    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'publishers'


class PublisherBook(models.Model):

    book = models.ForeignKey(Book, db_column='book')
    publisher = models.ForeignKey(Publisher, db_column='publisher')

    class Meta:
        db_table = 'books_publishers_link'


class Tag(models.Model):

    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'tags'


class TagBook(models.Model):

    book = models.ForeignKey(Book, db_column='book')
    tag = models.ForeignKey(Tag, db_column='tag')

    class Meta:
        db_table = 'books_tags_link'
        unique_together = ['book', 'tag']


class Series(models.Model):

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'series'


class SeriesBook(models.Model):

    book = models.ForeignKey(Book, db_column='book',
                             related_name='book_series', unique=True)
    series = models.ForeignKey(Series, db_column='series')

    class Meta:
        db_table = 'books_series_link'


class CustomColumnManager(models.Manager):

    def get_queryset(self):
        qs = super(CustomColumnManager, self).get_queryset()
        return qs.filter(data_type='bool')


class CustomColumn(models.Model):

    label = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=255, db_column='datatype')
    mark_for_delete = models.BooleanField(default=False)
    editable = models.BooleanField(default=False)
    display = models.CharField(max_length=255)
    is_multiple = models.BooleanField(default=False)
    normalized = models.BooleanField(default=False)

    @classmethod
    def create_models(cls):
        for column in cls.objects.all():
            book_field = models.ForeignKey(
                Book, db_column='book', related_name='custom_column_%s' %
                                                     column.label)
            if column.data_type == 'bool':
                model_field = models.BooleanField(default=False)
            else:
                model_field = models.CharField(max_length=255)
            fields = {
                'value':  model_field,
                'custom_column': column,
            }
            if not column.normalized:
                fields.update({'book': book_field})
            options = {'db_table': 'custom_column_%s' % column.id}
            create_model('CustomColumn%s' % column.id, fields,
                         options=options, module=__name__)
            if column.normalized:
                fields = {
                    'book': book_field,
                    'value': models.ForeignKey('CustomColumn%s' % column.id,
                                               db_column='value')}
                options = {
                    'db_table': 'books_custom_column_%s_link' % column.id}
                create_model('BookCustomColumn%s' % column.id, fields,
                             options=options, module=__name__)

    class Meta:
        db_table = 'custom_columns'

    def __unicode__(self):
        return self.name

try:
    CustomColumn.create_models()
except OperationalError:
    pass
