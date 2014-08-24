from haystack import indexes

from .models import Book


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)

    def get_model(self):
        return Book

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare(self, obj):
        self.prepared_data = super(BookIndex, self).prepare(obj)
        text = [obj.title, obj.isbn, obj.uuid]
        text.extend(obj.authors.all())
        text.extend(obj.tags.all())
        text.extend(obj.publishers.all())
        self.prepared_data['text'] = u' '.join(map(unicode, text))
        return self.prepared_data
